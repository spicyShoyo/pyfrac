from django.http import HttpResponse
from django.template import loader
from django.template.loader import render_to_string
from juliasuper import JuliaSuper
from mandelbrotsequential import MandelbrotSequential
from mandelbrotsuper import MandelbrotSuper

FRAC_TYPE_DIC = {"Julia": JuliaSuper, "MandelbrotSequential": MandelbrotSequential, "Mandelbrot": MandelbrotSuper}


def index(request):
    '''
    The indxe view
    :param request: http request
    :return: http response
    '''
    return query(request)


def query(request):
    '''
    The query view
    :param request: http request
    :return: http response
    '''
    template = loader.get_template('frac/frac2.html')
    project_list = []
    context = {
        'project_list': project_list,
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
    a = FRAC_TYPE_DIC[frac_type](x_res, y_res, x_min, x_max, y_min, y_max)
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
    }

    return getfrac_ajax(context)
