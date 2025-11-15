from django.shortcuts import render


def blogboard(request):
    return render(request, 'main/blog-main.html')


def Real_Estate_MoneyBall(request):
    return render(request, 'main/blogs/Real_Estate_MoneyBall.html')


def test_blog(request):
    return render(request, 'main/blogs/test.html')


def Tech_is_an_Arms_Race(request):
    return render(request, 'main/blogs/Tech_is_an_Arms_Race.html')


def The_Holy_Grail_of_Real_Estate(request):
    return render(request, 'main/blogs/The_Holy_Grail_of_Real_Estate.html')


def scalability(request):
    return render(request, 'main/blogs/scalability.html')
