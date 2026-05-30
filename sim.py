import itertools
import fresnel
import math
import hoomd
import numpy 
import gsd.hoomd
from PIL import Image
import imageio
import os

def render(positions, orientations, box_length):
    """
    Renders a 3D scene of particles inside a box using Fresnel.
    """
    scene = fresnel.Scene()
    geometry = fresnel.geometry.Sphere(scene, N=len(positions))
    geometry.position[:] = positions
    geometry.radius[:] = [0.4] * len(positions)
    
    geometry.material = fresnel.material.Material(
        color=fresnel.color.linear([0.2, 0.5, 0.8]),
        roughness=0.3,
        specular=0.5
    )
    
    geometry.outline_width = 0.0
    scene.camera = fresnel.camera.Orthographic.fit(scene)
    
    scene.lights = [
        fresnel.light.Light(direction=[1, 1, 1], color=[0.9, 0.9, 0.9], theta=0),
        fresnel.light.Light(direction=[-1, -1, 1], color=[0.3, 0.3, 0.3], theta=0)
    ]

    image = fresnel.preview(scene, w=600, h=600)
    img = Image.fromarray(image[:, :, 0:3], mode='RGB')
    return img

class LiveRenderer(hoomd.custom.Action):
    """
    A custom HOOMD-blue action that renders both MD Solute (Blue) 
    and MPCD Solvent (Red) on the fly.
    """
    def __init__(self, N_solute, max_solvent_render=13107, output_dir="./Renders/live_frames/"):
        self.N_solute = N_solute
        self.max_solvent_render = max_solvent_render
        self.output_dir = output_dir
        self.frame_count = 0
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Total maximum spheres we expect to render
        self.total_spheres = self.N_solute + self.max_solvent_render
        
        self.scene = fresnel.Scene()
        self.geometry = fresnel.geometry.Sphere(self.scene, N=self.total_spheres)
        
        # Set radii: Solutes are larger (0.5), Solvent particles are smaller points (0.15)
        radii = numpy.zeros(self.total_spheres)
        radii[:self.N_solute] = 0.5
        radii[self.N_solute:] = 0.15
        self.geometry.radius[:] = radii
        
        self.geometry.material = fresnel.material.Material(
            primitive_color_mix=1.0,
            roughness=0.3,
            specular=0.5
        )
        self.geometry.outline_width = 0.0
        
        self.scene.lights = [
            fresnel.light.Light(direction=[1, 1, 1], color=[0.9, 0.9, 0.9], theta=0),
            fresnel.light.Light(direction=[-1, -1, 1], color=[0.3, 0.3, 0.3], theta=0)
        ]
        
        # --- FIXED COLORS ---
        self.color_solute = [0.15, 0.55, 0.85]   # Solute = Blue
        self.color_solvent = [0.85, 0.15, 0.15]  # Solvent = Red

    def act(self, timestep):
        snap = self._state.get_snapshot()
        
       
        solute_pos = snap.particles.position[:self.N_solute]
        
      
        solvent_pos_all = snap.mpcd.position
        N_solvent_actual = min(len(solvent_pos_all), self.max_solvent_render)
        solvent_pos = solvent_pos_all[:N_solvent_actual]
        
        
        combined_pos = numpy.zeros((self.total_spheres, 3))
        combined_pos[:self.N_solute] = solute_pos
        combined_pos[self.N_solute:self.N_solute + N_solvent_actual] = solvent_pos
        self.geometry.position[:] = combined_pos
        
       
        colors = numpy.zeros((self.total_spheres, 3))
        colors[:self.N_solute] = self.color_solute  
        colors[self.N_solute:] = self.color_solvent  
        self.geometry.color[:] = fresnel.color.linear(colors)
        

        radii = numpy.zeros(self.total_spheres)
        radii[:self.N_solute] = 0.5
        radii[self.N_solute:self.N_solute + N_solvent_actual] = 0.15
        self.geometry.radius[:] = radii

        if self.frame_count == 0:
            self.scene.camera = fresnel.camera.Orthographic.fit(self.scene)

        image_array = fresnel.preview(self.scene, w=600, h=600)
        rgb_array = numpy.array(image_array[:, :, 0:3], dtype=numpy.uint8)
        img = Image.fromarray(rgb_array, mode='RGB')
        
        filename = os.path.join(self.output_dir, f"frame_{self.frame_count:04d}.png")
        img.save(filename)
        print(f"Live Render: Saved {filename} at timestep {timestep} (Solutes: {self.N_solute}, Solvent: {N_solvent_actual})")
        
        self.frame_count += 1