import os
import streamlit.components.v1 as components
import random

buildDir  = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend/build')

render_function = components.declare_component(
        "vizualization_3DT",
        url="http://localhost:3000",
        
        #path=buildDir
    )
 
def run_visualization(tilesetIPFS,Xcoordinate, Ycoordinate, username ):
    """
    this runs the 3D visualization on the giro3D engine
    
    Parameters
    –––––––––––
    
   tilesetIPFS: is the  cid script used to render the components
   Xcoordinate: is the lattitude from which you want to render the given tileset
   Ycoordinate: is the longitude from which you want to render the given tileset
   username: is the entity that has called the function
   Returns: 
   fetches the rendered map with the settings to zoom or to visualize the given tileset more clearly    
    """
    call = random.randint(0,100)
    print("rendering of job started for{}".format(username))
    tilesetURL =  'https://' + tilesetIPFS + '.ipfs.w3s.link/'  + '/pipeline_template.json'
    rendered_result = render_function(Xcoord=Xcoordinate,Ycoord=Ycoordinate,tilesetURL=tilesetURL,key="visualization_3DT", default=0)
    call += 1
    print("rendering of job finished for{}".format(username))
    return rendered_result