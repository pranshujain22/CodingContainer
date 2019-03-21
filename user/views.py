from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls.base import reverse
from django.shortcuts import render
from django.contrib import messages
from user.forms import UserForm
from user.models import UserProfile
import requests
import json


base_url = "http://spr.openport.io:38851"
token = "Token 4147d4512235bf845a7e8111a6c934cc5c416024"
# base_url = "http://localhost:8000"


def initial_setup(request):
    url = "https://spr.openport.io/l/38851/pJRvcymEglvid1LO"
    payload = ""
    headers = {
        'cache-control': "no-cache",
        'Postman-Token': "a1ec5098-d35b-4422-ba8b-e84baf36fe6c"
    }
    response = requests.request("GET", url, data=payload, headers=headers)
    return HttpResponseRedirect(reverse('user:index'))


def index(request):
    if request.method == "POST":
        print(request.POST)
    message = None
    for msg in messages.get_messages(request):
        message = msg
        break

    if 'enrollment_id' in request.session:
        return render(request, 'user/index.html', {'loggedIn': True, 'message': message})

    return render(request, 'user/index.html', {'message': message})


def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.password = make_password(request.POST.get('password'))
            user.save()

            url = base_url + "/api/v2/users/"
            payload = json.dumps({"user_id": request.POST.get('enrollment_id')})
            headers = {
                'Authorization': token,
                'Content-Type': "application/json",
                'cache-control': "no-cache",
            }

            response = requests.request("POST", url, data=payload, headers=headers)
            print(response.status_code)
            print(response.text)

            registered = True
            messages.add_message(request, messages.INFO, 'Registration completed. Login to continue...')
            return HttpResponseRedirect(reverse('user:login'))

        else:
            print(user_form.errors)
            message = None
            if 'Enrollment' in str(user_form.errors):
                message = 'User already exists with this Enrollment Id'
            else:
                message = 'User already exists with this Email'
            if 'Enrollment' in str(user_form.errors) and 'Email' in str(user_form.errors):
                message = 'User already exists with this Enrollment Id and Email'

            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('user:register'))

    if 'enrollment_id' in request.session:
        return HttpResponseRedirect(reverse('user:index'))

    message = None
    for msg in messages.get_messages(request):
        message = msg
        break

    return render(request, 'user/register.html', {'registered': registered, 'message': message})


def login(request):
    if request.method == "POST":
        enrollment_id = int(request.POST.get('enrollment_id'))
        password = request.POST.get('password')

        if enrollment_id in list(UserProfile.objects.values_list('pk', flat=True)):
            user = UserProfile.objects.get(enrollment_id=enrollment_id)

            if check_password(password, user.password):
                request.session['enrollment_id'] = user.enrollment_id
                request.session['username'] = user.username
                request.session['email'] = user.email
                messages.add_message(request, messages.INFO, 'Logged In Successfully')
                return HttpResponseRedirect(reverse('user:dashboard'))
            else:
                messages.add_message(request, messages.INFO, 'Invalid Credentials')
                return HttpResponseRedirect(reverse('user:login'))

        else:
            messages.add_message(request, messages.INFO, 'User Does Not Exists')
            return HttpResponseRedirect(reverse('user:login'))

    if 'enrollment_id' in request.session:
        return HttpResponseRedirect(reverse('user:index'))

    message = None
    for msg in messages.get_messages(request):
        message = msg
        break

    return render(request, 'user/login.html', {'message': message})


def logout(request):
    try:
        del request.session['enrollment_id']
        del request.session['username']
        del request.session['mail']
    except KeyError as err:
        print(err)

    messages.add_message(request, messages.INFO, 'Logged Out Successfully')
    return HttpResponseRedirect(reverse('user:index'))


def dashboard(request):
    return HttpResponseRedirect(reverse('user:containers'))
    # message = None
    # for msg in messages.get_messages(request):
    #     message = msg
    #     break
    #
    # if 'enrollment_id' in request.session:
    #     return render(request, 'user/dashboard.html', {'loggedIn': True, 'message': message})
    #
    # return render(request, 'user/dashboard.html', {})


def containers(request):
    message = None
    for msg in messages.get_messages(request):
        message = msg
        break

    if 'enrollment_id' not in request.session:
        messages.add_message(request, messages.INFO, 'You are not logged in..!')
        return HttpResponseRedirect(reverse('user:index'))

    return render(request, 'user/containers.html')


def profile(request):
    if 'enrollment_id' not in request.session:
        return HttpResponseRedirect(reverse('user:index'))

    return render(request, 'user/profile.html')


def images(request):
    url = base_url + "/api/v2/images/"

    headers = {
    'Authorization': token,
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    }

    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    print(response.text)
    if response.status_code == 200:
        images = dict()
        data = json.loads(response.text)
        for i in range(len(data)):
            images[i] = data[i]['name']

        return JsonResponse(images)

    return JsonResponse("Something went wrong!")


def create_container(request):
    if request.method == "POST":
        url = base_url + "/api/v2/containers/"
        print(request.POST)
        payload = json.dumps({
            "user_id": request.POST.get('user_id'),
            "image": request.POST.get('image'),
            "name": request.POST.get('name').lower()
        })
        headers = {
            'Authorization': token,
            'Content-Type': "application/json",
            'cache-control': "no-cache",
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        print(response.status_code)
        # print(response.text)
        data = json.loads(response.text)
        data['local_ports'] = json.loads(data['local_ports'])
        return JsonResponse(data)

    return JsonResponse({})


def get_containers(request):

    url = base_url + "/api/v2/users/" + str(request.session['enrollment_id'])
    headers = {
        'Authorization': token,
        'cache-control': "no-cache",
    }
    response = requests.request("GET", url, headers=headers)
    # print(response.text)
    print(response.status_code)

    containers_data = (json.loads(response.text))['containers']
    data = dict()
    for i in range(len(containers_data)):
        containers_data[i]['local_ports'] = json.loads(containers_data[i]['local_ports'])
        if containers_data[i]['external_ports'] != '':
            containers_data[i]['external_ports'] = json.loads(containers_data[i]['external_ports'])
        data[i] = containers_data[i]
        # print(containers_data[i])

    return JsonResponse(data)


def remove_container(request):
    if request.method == "GET":
        url = base_url + "/api/v2/containers/" + request.GET.get('container_id') + "/"
        headers = {
            'Authorization': token,
            'cache-control': "no-cache",
        }

        response = requests.request("DELETE", url, headers=headers)
        print(response.text)

        return JsonResponse({'result': "Deleted Successfully"})

    return JsonResponse({'result': "Some Error occurred"})


def open_port(request):
    if request.method == "GET":
        container_id = str(request.GET.get('container_id'))
        port = str(request.GET.get('port'))

        url = base_url + "/api/v2/openport/" + container_id + '/' + port
        payload = json.dumps({})

        headers = {
            'Authorization': token,
            'Content-Type': "application/json",
            'cache-control': "no-cache",
        }

        response = requests.request("GET", url, data=payload, headers=headers)
        print(json.loads(response.text))

        return JsonResponse({'ip': json.loads(response.text)[port]})

    return JsonResponse({'result': 'Some error occurred'})


def change_password(request):
    changed = False
    enrollment_id = int(request.POST.get('enrollment_id'))
    current_password = request.POST.get('current_password')
    new_password = request.POST.get('new_password')

    if request.method == "POST":
        user = UserProfile.objects.get(enrollment_id=enrollment_id)

        if not check_password(current_password, user.password):
            return JsonResponse({'changed': changed, 'current_password': 'wrong'})
        else:
            user.password = make_password(new_password)
            user.save()
            changed = True
            return JsonResponse({'changed': changed, 'current_password': 'matched'})

    return JsonResponse({'changed': changed, 'current_password': 'wrong'})


def files(request):
    if 'enrollment_id' not in request.session:
        return HttpResponseRedirect(reverse('user:index'))

    return render(request, 'user/files.html')


def editor(request):
    if 'enrollment_id' not in request.session:
        return HttpResponseRedirect(reverse('user:index'))

    if request.method == "GET":
        path = request.GET.get('path')
    else:
        path = request.POST.get('path')

    if path is None:
        return HttpResponseRedirect(reverse('user:index'))

    return render(request, 'user/editor.html', context={'path': path, 'container_id': request.GET.get('container_id')})


def get_directory(request):
    if request.method == "GET":
        container_id = str(request.GET.get('container_id'))

        url = base_url + "/api/v2/files/" + container_id
        payload = json.dumps({})

        headers = {
            'Authorization': token,
            'Content-Type': "application/json",
            'cache-control': "no-cache",
        }

        response = requests.request("GET", url, data=payload, headers=headers)
        json_acceptable_string = response.text.replace("'", "\"")
        directory = json.loads(json_acceptable_string)
        print(directory)
        if directory == {}:
            result = 'empty'
        else:
            result = 'success'

        return JsonResponse({'directory': directory, 'result': result})

    else:
        return JsonResponse({'result': 'err'})


@csrf_exempt
def edit_file(request):
    if request.POST.get('data') is None:

        url = base_url + "/api/v2/get_file"
        payload = {
            'container_id': request.POST.get('container_id'),
            'path': request.POST.get('path')
        }

        headers = {
            'Authorization': token,
            'cache-control': "no-cache",
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        if json.loads(response.text)['data'] == 'err':
            return JsonResponse({'data': 'err'})

        return JsonResponse({'data': json.loads(response.text)['data']})

    else:
        url = base_url + "/api/v2/post_file"
        payload = {
            'container_id': request.POST.get('container_id'),
            'path': request.POST.get('path'),
            'data': json.dumps(request.POST.get('data'))
        }

        headers = {
            'Authorization': token,
            'cache-control': "no-cache",
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        if json.loads(response.text)['data'] == 'err':
            return JsonResponse({'data': 'err'})

        return JsonResponse({'data': json.loads(response.text)['data']})

