from django.shortcuts import render,redirect
from django.http import HttpResponse
import markdown2 as md
from . import util
import secrets                              

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def wikipage(request,title):
    if title in util.list_entries():
        return render(request,"encyclopedia/page.html",{
        "info":md.markdown(util.get_entry(title)),
        "entry":title
        })
    else: 
        return render(request,"encyclopedia/error.html",{
            "error":"PAGE NOT FOUND!"
        })
def newpage(request):
    if request.method == "POST":
        title=request.POST.get("title")
        content=request.POST.get("content")
        if title==None:
            return render(request,"encyclopedia/newpage.html", {"error":"Title can't be blank"})
        if title in util.list_entries():
            return render(request,"encyclopedia/newpage.html", {"error":title+ " already exists!"})
        else:
            util.save_entry(title, content)
        return redirect('wikipage',title=title)
            
    return render(request,"encyclopedia/newpage.html")

def random(request):
    title=secrets.choice(util.list_entries())
    return redirect('wikipage', title=title)

def edit(request,title):
    if request.method == "POST":
        content=request.POST.get("content")
        util.save_entry(title, content)
        return redirect('wikipage',title=title)
    else:
        return render(request,"encyclopedia/edit.html",{
            "content":util.get_entry(title),
            "title":title
        })
def search(request):
    search=request.POST.get("search")
    if search==None:
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

    l=[]
    for a in util.list_entries():
        if a==search:
            return redirect('wikipage',title=search)
        if a.find(search) != -1:
            l.append(a)
    return render(request,"encyclopedia/search.html",{
        "lists":l
    })
        
