from django.shortcuts import render


def home(request):
    speakers = [
        {'name': 'Grace Hopper', 'photo': 'https://www.timeforkids.com/wp-content/uploads/2020/08/Grace_003.jpg'},
        {'name': 'Alan Turing', 'photo': 'https://cdn.britannica.com/81/191581-050-8C0A8CD3/Alan-Turing.jpg'},
    ]
    return render(request, 'index.html', {'speakers': speakers})


