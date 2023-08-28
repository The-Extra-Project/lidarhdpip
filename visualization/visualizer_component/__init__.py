import os
import streamlit.components.v1 as components


buildDir  = os.path.join(os.path.abspath(__file__), 'frontend/build/giro3D')

render_function = components.declare_component(
        "visualizer_component",
        path= buildDir
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
    
    tilesetURL =  'https://' + tilesetIPFS + '.ipfs.w3s.link/' + username + '/pipeline_template.json'
    rendered_result = render_function(tilesetURL=tilesetIPFS,Xcoord=Xcoordinate,Ycoord=Ycoordinate)
    return rendered_result
