from django.http import HttpResponse
from django.template import loader
from django.template.loader import render_to_string
from julia import Julia
from mandelbrot import Mandelbrot
from burningship import BurningShip
from demo import Demo
from fracgif import FracGIF
from perlin import Perlin
from blur import Blur
from diamondsquare import Diamondsquare

from frac.models import User, Images
import frac.models as db

FRAC_TYPE_DIC = {"Julia": Julia, "Mandelbrot": Mandelbrot, "Demo": Demo, "BurningShip": BurningShip}
NOISE_TYPE_DIC = {"Blur": Blur, "Diamondsquare": Diamondsquare, "Perlin": Perlin}

def index(request):
    '''
    The indxe view
    :param request: http request
    :return: http response
    '''
    return query(request)


def imgset(request):
    '''
    get the saved image set
    :param request: http request
    :return: a list of image source
    '''
    print(request)
    username = request.POST['username']
    template = loader.get_template('frac/imgset.html')
    imgset = db.get_img(username)
    print(imgset)
    context = {
        "img_list": imgset,
    }
    return HttpResponse(template.render(context, request))


def saved(request):
    '''
    The saved view
    :param request: http request
    :return: http response
    '''
    template = loader.get_template('frac/saved.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

def signin(request):
    '''
    The get signin api
    :param request: http post request
    :return: http response
    '''
    username = request.POST['username']
    password = request.POST['password']
    actiontype = request.POST['actiontype']
    if actiontype == "login":
        res = db.log_in(username, password)
    else:
        res = db.sign_up(username, password)
    html = "<p>" + str(res) + "</p>"
    return HttpResponse(html)


def query(request):
    '''
    The query view
    :param request: http request
    :return: http response
    '''
    template = loader.get_template('frac/frac.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

def getfrac_ajax(context):
    '''
    The get frac api helper
    response to ajax
    :param context: the context to be rendered by the template
    :return: http response
    '''
    html = render_to_string('frac/fraczoom.html', context)
    return HttpResponse(html)

def getfrac(request):
    '''
    The get frac api
    :param request: http post request
    :return: http response
    '''
    print(request.POST)
    token = request.POST["csrfmiddlewaretoken"]
    frac_type = request.POST["fractype"]
    x_res = int(request.POST["xres"])
    y_res = int(request.POST["yres"])
    x_min = float(request.POST["xmin"])
    x_max = float(request.POST["xmax"])
    y_min = float(request.POST["ymin"])
    y_max = float(request.POST["ymax"])
    cr = float(request.POST["cr"])
    ci = float(request.POST["ci"])
    typefield = request.POST["typefield"]
    if typefield == "zoom":
        a = FRAC_TYPE_DIC[frac_type](x_res, y_res, x_min, x_max, y_min, y_max, cr, ci)
        a.solve()
        fn = a.save_img()

        context = {
            'img_src': fn,
            'token': token,
            'frac_type': frac_type,
            'x_res': x_res,
            'y_res': y_res,
            'x_min': x_min,
            'x_max': x_max,
            'y_min': y_min,
            'y_max': y_max,
            'cr': cr,
            'ci': ci,
        }

        return getfrac_ajax(context)
    else:
        a = FracGIF(frac_type, x_res, y_res, x_min, x_max, y_min, y_max, cr, ci)
        a.solve()
        fn = a.save_gif()

        context = {
            'img_src': fn,
            'token': token,
            'frac_type': frac_type,
            'x_res': x_res,
            'y_res': y_res,
            'x_min': x_min,
            'x_max': x_max,
            'y_min': y_min,
            'y_max': y_max,
            'cr': cr,
            'ci': ci,
        }

        return getfrac_ajax(context)

def getnoise_ajax(context):
    '''
    The get noise api helper
    response to ajax
    :param context: the context
    :return: http response
    '''
    html = render_to_string('frac/noiseshow.html', context)
    return HttpResponse(html)

def getnoise(request):
    '''
    The get noise api
    :param request: http post request
    :return: http response
    '''
    token = request.POST["csrfmiddlewaretoken"]
    noise_type = request.POST["noisetype"]
    res = int(request.POST["res"])
    smoothp = int(request.POST["smoothp"])
    n = int(request.POST["n"])
    smoothd = float(request.POST["smoothd"])
    a = None
    if noise_type == "Blur":
        a = NOISE_TYPE_DIC[noise_type](res, smoothp)
    elif noise_type == "Perlin":
        a = NOISE_TYPE_DIC[noise_type](res)
    else:
        a = NOISE_TYPE_DIC[noise_type](n, smoothd)
    a.solve()
    fn = a.save_img()
    context = {
    'token': token,
        'img_src': fn,
        'noisetype': noise_type,
    }
    return getnoise_ajax(context)

def noise(request):
    '''
    The noise view
    :param request: http request
    :return: http response
    '''
    template = loader.get_template('frac/noise.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

def addimg(request):
    '''
    The addimg api
    :param request: http request
    :return: http response
    '''
    db.add_img(request.POST)
    print(request.POST)
    return HttpResponse("<p>added</p>")
