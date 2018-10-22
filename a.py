import os
from flask import Flask, Response, request, abort, render_template_string, render_template, send_from_directory
from PIL import Image
import StringIO # Use Python2 ; StringIO becomes io in Python3. Check out online

app = Flask(__name__)

WIDTH = 640
HEIGHT = 360

# HTML Template that you want to render
# Can also load as a separate HTML file but shoudl store in ./templates/ folder else Flask will not recognize

TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
<title></title>
<meta charset="utf-8" />
<style>
body {
margin: 0;
background-color: #333;
}

#icons{float:left;
    width: 64px; 
    height: 64px;
    margin:5px;
   }
   
.image {
display: inline-block;
margin: 3em 14px;
background-color: #FFF;
box-shadow: 0 0 10px rgba(0,0,0,0.0);
}
img {
display: block;
}
</style>
<script src="https://code.jquery.com/jquery-1.10.2.min.js" charset="utf-8"></script>
<script src="http://luis-almeida.github.io/unveil/jquery.unveil.min.js" charset="utf-8"></script>
<script>

$(document).ready(function() {
$('img').unveil(1000);
});
</script>
</head>
<body>

<input type="reset" value="REFRESH">

<table border = 1>

{% for image in images %}
    
    <tr>
               <td> <a class="image" href="{{ image.src }}" >
        <img src="{{ image.src }}" data-src="{{ image.src }} height="64" width="64"/>
        
    </a></td>
               <td> <a class="image" href="{{ image.src }}" >
        <img src="{{ image.src }}" data-src="{{ image.src }} height="64" width="64"/>
        
    </a></td>
    <td> <a class="image" href="{{ image.src }}" >
        <img src="{{ image.src }}" data-src="{{ image.src }} height="64" width="64"/>
        
    </a></td>
    
     </tr>
     <div id="icons"><a class="image" href="{{ image.src }}" >
        <img src="{{ image.src }}" data-src="{{ image.src }} height="64" width="64"/>
        
    </a></div>
{% endfor %}
      </table>
      
      
</body>
'''
# Rendering Images
@app.route('/<path:filename>')

def image(filename):
	print ("filename")
	try:
		w = int(request.args['w'])
		h = int(request.args['h'])
	except (KeyError, ValueError):
		return send_from_directory('.', filename)

	try:
		im = Image.open(filename)
		im.thumbnail((w, h), Image.ANTIALIAS)
		io = StringIO.StringIO()
		im.save(io, format='JPEG')
		return Response(io.getvalue(), mimetype='image/jpeg')

	except IOError:
		abort(404)

	return send_from_directory('.', filename)


#Main Directory *Page that will be rendered by URl
@app.route('/')
def index():
	images = []
	for root, dirs, files in os.walk('./images/'):
		files.sort()
		for filename in [os.path.join(root, name) for name in files]:
			print (filename)
			if not (filename.endswith('.jpeg') or filename.endswith('.png') or filename.endswith('.jpg')):
				continue
			im = Image.open(filename)
			images.append({
				'src': filename
			})
		
# 	return render_template_string(TEMPLATE, **{'images':images})  # In case you want to Load the HTML that is stored in the string TEMPLATE
	return render_template("x.html", **{'images':images})      #Loading from the html file "x.html"
	
	
if __name__ == '__main__':

	app.run(host="0.0.0.0", port="3000", debug = True)  
	
	#URL and Port # When Debug is true Webpage will reload whenever there is some change in the File
