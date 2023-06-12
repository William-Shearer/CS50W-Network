from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, DataError, DatabaseError
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
# from django.views.decorators.csrf import csrf_exempt # This doesn't even work sometimes. Garbage! Utter clutter garbage. Ignore it. Complete WASTE OF TIME.
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
import json


def index(request):
    if request.method == "GET":
        form = PostForm()
        # edit_form = EditPostForm()
        posts = Post.objects.all().order_by("-date_created")
        paginator = Paginator(posts, 10)
        page = request.GET.get("page")
        post_set = paginator.get_page(page)
        profiles = Profile.objects.all()
        #content = {"form": form, "posts": posts}
        #form_content = {"form": form, "edit_form": edit_form, "posts": post_set}
        form_content = {"form": form, "posts": post_set, "profiles": profiles}
        #content = {"posts": posts}
    elif request.method == "POST":
        form = PostForm(request.POST or None)
        if form.is_valid():
            subject = form.cleaned_data.get("subject")
            content = form.cleaned_data.get("content")
            try:
                if request.user is not None:
                    Post.objects.create(author = request.user, subject = subject, content = content) #content = bytes(content, "utf8"))
            except IntegrityError:
                print("Cannot make that")
            else:
                print("Post OK")
            finally:
                return redirect(reverse("index"))

    return render(request, "network/index.html", form_content)


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            # Attempt to sign user in
            #username = request.POST["username"]
            #password = request.POST["password"]
            user = authenticate(request, username = username, password = password)

            # Check if authentication successful
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                content = {"form": LoginForm(), "message": "Invalid username and/or password."}
                return render(request, "network/login.html", content)
                #return render(request, "network/login.html", {
                #    "message": "Invalid username and/or password."
                #})
    else: # GET
        form = LoginForm()
        content = {"form": form}
        return render(request, "network/login.html", content)

# Kind of obvious, and it wouldn't do any harm if a logout was invoked while not
# logged in, but in the event it could be used some way to break the server,
# here it is...
@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        # username = request.POST["username"]
        # email = request.POST["email"]
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            biography = form.cleaned_data.get("biography")
            userimage = form.cleaned_data.get("userimage")
            password = form.cleaned_data.get("password")
            confirmation = form.cleaned_data.get("confirmation")
            # Ensure password matches confirmation
            # password = request.POST["password"]
            # confirmation = request.POST["confirmation"]
            if password != confirmation:
                content = {"form": RegisterForm(), "message": "Passwords must match"}
                return render(request, "network/register.html", content)
                #return render(request, "network/register.html", {
                #    "message": "Passwords must match."
                #})

            # Attempt to create new user
            try:
                user = User.objects.create_user(username, email, password)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
            except IntegrityError:
                return render(request, "network/register.html", {
                    "message": "Username already taken."
                })
            else:
                Profile.objects.create(member = user, userimage = userimage, biography = biography)
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
    else:
        content = {"form": RegisterForm()}
        return render(request, "network/register.html", content)


@login_required
def change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.POST or None)
        if form.is_valid():
            password = form.cleaned_data.get("password")
            confirmation = form.cleaned_data.get("confirmation")
            if password != confirmation:
                content = {"form": ChangePasswordForm(), "message": "Passwords must match"}
                return render(request, "network/changepassword.html", content)
            else:
                user = request.user
                try:
                    user.set_password(password)
                    user.save()
                    login(request, user)
                except (IntegrityError, ValidationError, DataError, DatabaseError) as error:
                    print(f"There was this error: {error}")

        return redirect(reverse("index"))

    else:
        content = {"form": ChangePasswordForm()}
        return render(request, "network/changepassword.html", content)


@login_required
def edit_profile(request):
    # Some data is in Profile, and some in User. Get both.
    profile = Profile.objects.get(member = request.user)
    member = User.objects.get(username = request.user.username)
    if request.method == "POST":
        # When dealing with uploaded files, add the request.FILES.
        # Also look at the editprofile.html file to see how this works.
        # The enctype needs to be added to the form attributes, it is important.
        form = EditProfileForm(request.POST or None)
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            biography = form.cleaned_data.get("biography")
            try:
                member.first_name = first_name
                member.last_name = last_name
                member.email = email
                profile.biography = biography
                member.save()
                profile.save()
            except IntegrityError as error:
                print(f"This here happened: {error}")
            else:
                #return redirect(reverse("index"))
                # Wrong place, needs to go back to the profile. Look again, this is
                # how to pass parameters with a redirect. The comma is important.
                return redirect(reverse("viewprofile", args=(request.user.id,)))

    else:
        """
        This is the best way to prepopulate forms, provided they are forms made with Django.
        That is an efficient way to create forms, in any case. There does not seem to be much
        sense in making hand crafted HTML forms when there is a tool like this available,
        accessible to both HTML and JavaScript, too.
        """
        form = EditProfileForm(initial =    {
                                                "first_name": member.first_name,
                                                "last_name": member.last_name,
                                                "email": member.email,
                                                "biography": profile.biography
                                            })
        content = {"form": form}
        return render(request, "network/editprofile.html", content)


# Don't need this anymore, it just messes up my own redirect protection.
#@login_required
def view_profile(request, user_id):
    user = request.user
    if user.is_authenticated:
        if request.method == "GET":
            member = User.objects.get(id = user_id)
            profile = Profile.objects.get(member = member)
            user_posts = Post.objects.filter(author = member).order_by("-date_created")
            paginator = Paginator(user_posts, 10)
            page = request.GET.get("page")
            user_posts_set = paginator.get_page(page)
            # This gets how many members the current profile follows.
            follows = member.profile_by_followed.count()
            # This gets how many members follow the current profile.
            #followed = profile.followed.all().count()
            # It will go somewhere else, now. Reason. Enable JavaScript edit of element.
            print(follows)
            # print(followed)
            content = {
                "member": member,
                "profile": profile,
                "follows": follows,
                #"followed": followed,
                "user_posts": user_posts_set}
        return render(request, "network/profile.html", content)
    else:
        return redirect(reverse("index"))


@login_required
def update_followed(request, member_id):
    if request.method == "GET":
        try:
            member = User.objects.get(id = member_id)
            user_name = member.username
            profile = Profile.objects.get(member = member)
            followed = profile.followed.all().count()
        except (IntegrityError, ValidationError, DataError, DatabaseError) as error:
            return HttpResponse(f"Error: {error}")
        else:
            return JsonResponse({"followed_count": followed, "user_name": user_name})
    else:
        return redirect(reverse("index"))


@login_required
def like_post(request, post_id):
    user = request.user
    if request.method == "PUT":
        post = Post.objects.get(id = post_id)
        if user != post.author:
            likes = post.liked.all()
            if user in likes:
                post.liked.remove(user)
                print(f"Unliking the post by {post.author.username}")
            else:
                post.liked.add(user)
                print(f"Liking the post by {post.author.username}")

            liked_count = {"liked_count": post.liked.count()}
            return JsonResponse(liked_count)
        else:
            print("Crime commited: You like yourself. Bad. Very bad.")
            return HttpResponse("Liking yourself is prohibited")


"""
Not much to say here, but what little is probably important.
And it is this... the jscript.js function to reference is get_like. It
contains a fetch GET request, which this sends back as a JSON response.
Here is not so bad, straight forward familiar Django GET. And, for a change,
the fetch request over there is not the end of the world, either. Good,
refresh start point, this little pair, if forgetfulness prowls the cranium.
"""
# login required a bit redundant? We'll see...
def get_likes(request, post_id):
    if request.method == "GET":
        like_count = Post.objects.get(id = post_id).liked.count()
        print(f"Count is: {like_count}")

        return JsonResponse({"like_count": like_count})
    else:
        return redirect(reverse("index"))


"""
This is not too hard to get one's head around, once the proper way to do
a PUT is figured out. It is a bit of a pain, but it is in my Django notes (part 3).
As usual, the problem is not here, in itself. It is in shuttling the information
around and making sure I have a real JSON string, and not a fake pseudo JSON dict
that needs the safeties setting to False. That makes my skin crawl. The jscript.js
file should be referenced, because the complicated stuff is there. The primary part
of the put_edit function should be looked at, because it also shows the way to transfer
the csrf_token, thereby avoiding csrf_exempt here, which also makes my skin crawl.
"""
@login_required
def put_edit(request, post_id):
    if request.method == "PUT":
        try:
            post = Post.objects.get(id = post_id)
            data = json.loads(request.body)
            # print(data["new_text"])
            # print(data["current_user"])
            # Yeah, this is where the final word on the specification
            # is accomplished. ANYONE, but the current_user editing an own post,
            # is rejected.
            if post.author.id == int(data["current_user"]):
                print("This is the legitimate user.")
                post.content = data["new_text"]
                post.save()
            else:
                print("Big fake user trying to edit another's post. Go away!")
                return HttpResponse("Hack attempt")
        except IntegrityError as error:
            print(f"Unable to edit: {error}")
            return HttpResponse("Error")
        finally:
            return HttpResponse("Done")
    else:
        return redirect(reverse("index"))


"""
Another API function. This one was kind of tricky, the
date format needed to mimic the HTML Template format, for one,
because this overrides the natural behavior of said HTML file (index).
But the real trickiness is over in the jscript.js file.
It is the put_edit function supplement fetch promise there,
nested in the if response.ok conditional of the primary
PUT request. Best look at that again, cross reference here.
It was all a bit of a minor mind warp... easy to forget what I did.
"""
@login_required
def get_editdate(request, post_id):
    if request.method == "GET":
        edit_date = Post.objects.get(id = post_id).last_edit
        # print(edit_date.strftime("%b %d, %Y"))
        format_date = edit_date.strftime("%b %d, %Y, %H:%M")
        return JsonResponse({"edit_date": format_date})
    else:
        return HttpResponse("Not Valid Request")

@login_required
def put_follow(request, member_id):
    if request.method == "PUT": # Which it should be...
        #put_data = json.loads(request.body)
        current_user = request.user
        member_profile = Profile.objects.get(member = member_id)

        if current_user in member_profile.followed.all():
            member_profile.followed.remove(current_user)
        else:
            member_profile.followed.add(current_user)

        return HttpResponse("BLANK")
    else:
        return HttpResponse("Something weird happening. This should be a PUT request.")

    # This should never happen, but stops any silly behavior by going back to index.
    return redirect(reverse("index"))


@login_required
def get_follow(request, member_id):
    if request.method == "GET":
        print(f"In get_follow with {member_id}")
        # member = User.objects.get(id = member_id) redundant.
        profile = Profile.objects.get(id = member_id)
        followers = list()
        for follower in profile.followed.all():
            followers.append({"member_id":follower.id})
        # JSON is actually a bigger pain in the backside than it initially appears.
        return JsonResponse({"followers": followers})
    else:
        # Should only EVER be GET requests here.
        return HttpResponse("Hey! That should not have happened!")

    # Default: Bug out back to Index.
    return redirect(reverse("index"))

@login_required
def user_follows_posts(request):
    if request.method == "GET":
        user = request.user
        follow_profiles = user.profile_by_followed.all()
        # print(f"User { user.username } follows { follow_profiles }")
        followed_names = []
        for prf in follow_profiles:
            followed_names.append(prf.member.username)

        followed_posts = Post.objects.filter(author__username__in = followed_names).order_by("-date_created")

        paginator = Paginator(followed_posts, 10)
        page = request.GET.get("page")
        posts = paginator.get_page(page)

        content = {"posts": posts, "profiles": follow_profiles}

        return render(request, "network/follow.html", content)
    else:
        print("Error, not a GET request. Look into why.")

    return redirect(reverse("index"))
