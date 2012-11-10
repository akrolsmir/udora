from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from pantube.Udora import Udora
from django.utils import simplejson

U = None
vid = '9bZkp7q19f0'

def home(request):
	# return HttpResponse('HOME')
	return render_to_response('pantube/home.html',
     context_instance=RequestContext(request))

def video(request):
    global U, vid

    if request.method == 'POST':
        print "Making Udora"
        url = request.POST.get('url', 'invalid')
        if url != 'invalid':
            U = Udora(url)
            U.updateDict()
            U.getHighestURL()
            vid = U.getHighestURL()
            return render_to_response('pantube/index.html', {'firstVideo': vid})

        type = request.POST.get('type')
        print request.POST
        if type == 'get_next_video':
            video_id = U.getHighestURL()
            print 'video_id' + video_id
            return_dict = {'video_id': video_id}
            json = simplejson.dumps(return_dict)
            return HttpResponse(json, mimetype="application/json")
        elif type == 'thumbs_up':
            url = request.POST.get('video')
            U.changeRanking(True, url)
        elif type == 'thumbs_down':
            url = request.POST.get('video')
            U.changeRanking(False, url)
            video_id = U.getHighestURL()
            return_dict = {'video_id': video_id}
            json = simplejson.dumps(return_dict)
            return HttpResponse(json, mimetype="application/json")
        else:
            print 'Invalid type'
    # if request.method == 'get':
    #     return HttpResponse(request.read())
    # return HttpResponse('hi!')
    return render_to_response('pantube/index.html', {'firstVideo': vid})