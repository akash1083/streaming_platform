from django.contrib import messages
from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from urllib.parse import urlparse, parse_qs
from app.models import Register, Category, ShortFilm, WatchLater


# Create your views here.
def register(request):
    if request.method=="POST":
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        phone_no=request.POST.get("phone_no")
        if Register.objects.filter(username=username).exists():
            messages.error(request,"username already exist")
            return redirect("register")
        Register.objects.create(username=username,email=email,password=password,phone_no=phone_no)
        messages.success(request,"Registration successful")
        return redirect("login")
    return render(request,"register.html")


def login(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password = request.POST.get("password")
        user=Register.objects.filter(username=username,password=password).first()
        if user:
            request.session['user_id'] = user.id
            request.session["role"] = user.role
            messages.success(request, "Login successfully")

            if user.role == "admin":
                return redirect("admin_dashboard")
            else:
                return redirect("home")
        else:
            messages.error(request,"invalid username or password")
            return redirect("login")
    return render(request,"login.html")

def logout(request):
    request.session.flush()
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")


def add_category(request):
    if "user_id" not in request.session:
        return redirect("login")
    if request.session.get("role") != "admin":
        messages.error(request, "Access denied.")
        return redirect("home")
    if request.method == "POST":
        category_name = request.POST.get("category_name")
        Category.objects.create(category_name=category_name)
        return redirect("add_category")

    return render(request, "add_category.html")

def upload_film(request):
    if "user_id" not in request.session:
        return redirect("login")
    if request.session.get("role") != "admin":
        messages.error(request, "Access denied.")
        return redirect("home")
    categories = Category.objects.all()

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        duration = request.POST.get("duration")
        youtube_link = request.POST.get("youtube_link")
        category_id = request.POST.get("category")
        thumbnail = request.FILES.get("thumbnail")

        category = Category.objects.filter(id=category_id).first()


        if not category:
            messages.error(request, "Invalid category.")
            return redirect("upload_film")

        ShortFilm.objects.create(
            title=title,
            description=description,
            duration=duration,
            youtube_link=youtube_link,
            category=category,
            thumbnail=thumbnail,
        )

        messages.success(request, "Film uploaded successfully.")
        return redirect("upload_film")

    return render(request, "upload_film.html", {"categories": categories})


def home(request):
    if 'user_id' not in request.session:
        return redirect("login")

    films = ShortFilm.objects.all()

    return render(request, "home.html", {"films": films})


def film_details(request, id):
    if "user_id" not in request.session:
        return redirect("login")

    film = get_object_or_404(ShortFilm, id=id)
    user = Register.objects.get(id=request.session["user_id"])

    is_saved = WatchLater.objects.filter(
        user=user,
        shortfilm=film
    ).exists()

    url = film.youtube_link.strip()
    video_id = ""

    if "youtu.be/" in url:
        video_id = urlparse(url).path.lstrip("/")

    elif "watch?v=" in url:
        video_id = parse_qs(urlparse(url).query).get("v", [""])[0]

    elif "shorts/" in url:
        video_id = url.split("shorts/")[1].split("?")[0]

    elif "embed/" in url:
        video_id = url.split("embed/")[1].split("?")[0]

    embed_url = f"https://www.youtube.com/embed/{video_id}"

    return render(request, "film_details.html", {
        "film": film,
        "embed_url": embed_url,
        "is_saved": is_saved,
    })

def add_watch_later(request, id):
    if "user_id" not in request.session:
        return redirect("login")

    user = Register.objects.get(id=request.session["user_id"])
    film = get_object_or_404(ShortFilm, id=id)

    WatchLater.objects.get_or_create(
        user=user,
        shortfilm=film
    )

    messages.success(request, "Added to Watch Later")
    return redirect("film_details", id=id)

def watch_later(request):
    if "user_id" not in request.session:
        return redirect("login")

    user = Register.objects.get(id=request.session["user_id"])

    films = WatchLater.objects.filter(user=user)

    return render(request, "watch_later.html", {
        "films": films
    })

def remove_watch_later(request, id):
    if "user_id" not in request.session:
        return redirect("login")

    user = Register.objects.get(id=request.session["user_id"])

    WatchLater.objects.filter(
        user=user,
        shortfilm_id=id
    ).delete()

    messages.success(request, "Removed from Watch Later")
    return redirect("watch_later")

def admin_dashboard(request):
    if "user_id" not in request.session:
        return redirect("login")

    if request.session.get("role") != "admin":
        messages.error(request, "Access Denied")
        return redirect("home")

    context = {
        "users": Register.objects.count(),
        "categories": Category.objects.count(),
        "films": ShortFilm.objects.count(),
    }

    return render(request, "admin_dashboard.html", context)

def manage_films(request):
    if "user_id" not in request.session:
        return redirect("login")

    if request.session.get("role") != "admin":
        messages.error(request, "Access Denied")
        return redirect("home")

    films = ShortFilm.objects.all().order_by("-uploaded_at")

    return render(request, "manage_films.html", {
        "films": films
    })

def delete_film(request, id):
    if "user_id" not in request.session:
        return redirect("login")

    if request.session.get("role") != "admin":
        messages.error(request, "Access Denied")
        return redirect("home")

    film = get_object_or_404(ShortFilm, id=id)

    film.delete()

    messages.success(request, "Film deleted successfully.")

    return redirect("manage_films")

def edit_film(request, id):
    if "user_id" not in request.session:
        return redirect("login")

    if request.session.get("role") != "admin":
        messages.error(request, "Access Denied")
        return redirect("home")

    film = get_object_or_404(ShortFilm, id=id)
    categories = Category.objects.all()

    if request.method == "POST":

        film.title = request.POST.get("title")
        film.description = request.POST.get("description")
        film.duration = request.POST.get("duration")
        film.youtube_link = request.POST.get("youtube_link")

        category = Category.objects.get(id=request.POST.get("category"))
        film.category = category

        if request.FILES.get("thumbnail"):
            film.thumbnail = request.FILES.get("thumbnail")

        film.save()

        messages.success(request, "Film updated successfully.")

        return redirect("manage_films")

    return render(request, "edit_film.html", {
        "film": film,
        "categories": categories
    })

def manage_users(request):
    if "user_id" not in request.session:
        return redirect("login")

    if request.session.get("role") != "admin":
        messages.error(request, "Access Denied")
        return redirect("home")

    users = Register.objects.all().order_by("id")

    return render(request, "manage_users.html", {
        "users": users
    })


def change_role(request, id):
    if "user_id" not in request.session:
        return redirect("login")

    if request.session.get("role") != "admin":
        return redirect("home")

    user = get_object_or_404(Register, id=id)

    if user.role == "user":
        user.role = "admin"
    else:
        user.role = "user"

    user.save()

    messages.success(request, "User role updated successfully.")

    return redirect("manage_users")


def delete_user(request, id):
    if "user_id" not in request.session:
        return redirect("login")

    if request.session.get("role") != "admin":
        return redirect("home")

    user = get_object_or_404(Register, id=id)

    # Prevent admin from deleting themselves
    if user.id == request.session["user_id"]:
        messages.error(request, "You cannot delete your own account.")
        return redirect("manage_users")

    user.delete()

    messages.success(request, "User deleted successfully.")

    return redirect("manage_users")