
// credits to the example written by giro3D : https://giro3d.org/examples/colorized_pointcloud.html

import { Vector3 } from 'three';
import TileWMS from 'ol/source/TileWMS.js';
import { MapControls } from 'three/examples/jsm/controls/OrbitControls.js';
import Instance from '@giro3d/giro3d/core/Instance.js';
import Tiles3D from '@giro3d/giro3d/entities/Tiles3D.js';
import ColorLayer from '@giro3d/giro3d/core/layer/ColorLayer.js';
import PointsMaterial, { MODE } from '@giro3d/giro3d/renderer/PointsMaterial.js';
import Tiles3DSource from '@giro3d/giro3d/sources/Tiles3DSource.js';
import TiledImageSource from '@giro3d/giro3d/sources/TiledImageSource.js';
import Inspector from '@giro3d/giro3d/gui/Inspector.js';
import Extent from '@giro3d/giro3d/core/geographic/Extent.js';
import StatusBar from './utils/Statusbar';
import { Streamlit,
    StreamlitComponentBase,
  withStreamlitConnection
    ,RenderData } from "streamlit-component-lib";

import React , {ReactNode, useRef}  from "react";

interface passedParameters {
Xcoord: number
Ycoord: number
Url_tiles: string
}

let instance: Instance
let pointcloud : Tiles3D
let material : PointsMaterial
let Vector3d: Vector3
// defining the DOM elements
let viewerDiv
let pointcloud_render
let panelDiv

/*
functions for setting up the reference position ofr viewing the point cloud 
*/

function placeCamera(position, lookAt) {
    instance.camera.camera3D.position.set(position.x, position.y, position.z);
    instance.camera.camera3D.lookAt(lookAt);
    // create controls
    const controls = new MapControls(instance.camera.camera3D, instance.domElement);
    controls.target.copy(lookAt);
    controls.enableDamping = true;
    controls.dampingFactor = 0.25;

    instance.useTHREEControls(controls);

    instance.notifyChange(instance.camera.camera3D);
}

// add pointcloud to scene
function initializeCamera(url_tile) {
    const bbox = pointcloud.root.bbox
        ? pointcloud.root.bbox
        : pointcloud.root.boundingVolume.box.clone().applyMatrix4(pointcloud.root.matrixWorld);

    instance.camera.camera3D.far = 2.0 * bbox.getSize(Vector3d).length();

    const ratio = bbox.getSize(Vector3d).x / bbox.getSize(Vector3d).z;
    const position = bbox.min.clone().add(
        bbox.getSize(Vector3d).multiply({ x: 0, y: 0, z: ratio * 0.5 }),
    );
    const lookAt = bbox.getCenter(Vector3d);
    lookAt.z = bbox.min.z;

    const extent = Extent.fromBox3('EPSG:3946', bbox);

    placeCamera(position, lookAt);

    const colorize = new TiledImageSource({
        source: new TileWMS({
            url: url_tile,
            projection: 'EPSG:3946',
            params: {
                LAYERS: ['HR.ORTHOIMAGERY.ORTHOPHOTOS'],
                FORMAT: 'image/jpeg',
            },
        }),
    });

   const colorLayer = new ColorLayer(
        'wms_imagery',
        {
            extent,
            source: colorize,
        },
    );

    pointcloud.attach(colorLayer);

    instance.renderingOptions.enableEDL = true;
    instance.renderingOptions.enableInpainting = true;
    instance.renderingOptions.enablePointCloudOcclusion = true;

    StatusBar.bind(instance);
}




export class vizualization_3DT extends StreamlitComponentBase<passedParameters> {
    
    constructor() {
       super()
        Vector3d = new Vector3();
        
    }
    
    
    renderparameters = (tilesetURL: any = "", lat_1: string, lat_2: string) => {

        Instance.registerCRS('EPSG:2154',
        'proj=lcc +lat_1=45.25 +lat_2=46.75 +lat_0=46 +lon_0=3 +x_0=' + lat_1 +
        +'y_0=' + lat_2 +'ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs');
    
    viewerDiv = document.getElementById('viewerDiv') as HTMLElement ;
    pointcloud_render = document.getElementById('pointcloud_mode') as HTMLElement;
    panelDiv = document.getElementById('panelDiv') as HTMLDivElement
    
    instance = new Instance(viewerDiv, {
        crs: 'EPSG:2154',
        renderer: {
            clearColor: 0xcccccc,
        },
    });
    
    // Create a custom material for our point cloud.
     material = new PointsMaterial({
        size: 4,
        mode: MODE.TEXTURE,
    });
    
    
    
    // Create the 3D tiles entity
     pointcloud = new Tiles3D(
        'pointcloud',
        new Tiles3DSource(tilesetURL),
        {
            material,
        },
    );
    
    
    let colorLayer;
    
    
    instance.add(pointcloud).then(initializeCamera(tilesetURL) as any);
    
    Inspector.attach(panelDiv, instance);
    instance.domElement.addEventListener('dblclick', e => console.log(instance.pickObjectsAt(e, {
        radius: 5,
        // Limit the number of results for better performances
        limit: 10,
        // Some points are incoherent in the pointcloud, don't pick them
        filter: p => !Number.isNaN(p.point.z) && p.point.z < 1000,
    })));
    
    instance.notifyChange();
    
    function bindSlider(name, fn) {
        const slider = document.getElementById(name) as any;
        slider.oninput = function oninput() {
            fn(slider.value);
            instance.notifyChange();
        };
    
        Streamlit.setComponentValue(slider.value)
    }
    
    function bindToggle(name, action) {
        const toggle = document.getElementById(name) as any;
        toggle.oninput = () => {
            const state = toggle.checked;
            action(state);
            instance.notifyChange();
            Streamlit.setComponentValue(state)
        };
    }
    
    bindToggle('edl-enable', v => { instance.renderingOptions.enableEDL = v; });
    bindToggle('occlusion-enable', v => { instance.renderingOptions.enablePointCloudOcclusion = v; });
    bindToggle('inpainting-enable', v => { instance.renderingOptions.enableInpainting = v; });
    bindSlider('edl-radius', v => { instance.renderingOptions.EDLRadius = v; });
    bindSlider('edl-intensity', v => { instance.renderingOptions.EDLStrength = v; });
    bindSlider('inpainting-steps', v => { instance.renderingOptions.inpaintingSteps = v; });
    
    
    pointcloud_render.addEventListener('change', (e: any) => {
        const newMode = parseInt(e.target, 10);
        material.mode = newMode;
        instance.notifyChange(pointcloud, true);
        if (colorLayer) {
            colorLayer.visible = newMode === MODE.TEXTURE;
            instance.notifyChange(colorLayer, true);
        }
    });
    
    }
    

    public initialState: passedParameters = {
    Url_tiles: "",
    Xcoord: 0,
    Ycoord: 0,
}
    

public render = () : ReactNode => {
    const xCoord = this.props.args["Xcoord"]
    const yCoord = this.props.args["Ycoord"]
    const url = this.props.args["tilesetURL"]

    return(
        <div>
            renderingTiles(tilesetURL, xCoord, yCoord)

        </div>
    )

}



}

withStreamlitConnection(vizualization_3DT)

