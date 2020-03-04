# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 14:02:07 2019

@author: Fred.White
"""
# Python test with COM interface and Frew

import win32com.client
from pathlib import Path
import time
import matplotlib.pyplot as plt
import os
import matplotlib.backends.backend_pdf as pltexp

# Timer for script running
StartTime = time.time()

plt.close("all")

# Revert matplotlib to original settings
plt.rcParams.update(plt.rcParamsDefault)

font_size = 8
# Define global settings for figures
plt.rcParams.update({'font.size': font_size})
#plt.rcParams.update({'font.family': 'serif'})
#plt.rcParams.update({'font.serif': 'Times New Roman'})
plt.rcParams.update({'axes.titlesize': font_size})
#plt.rcParams.update({'axes.titleweight': 'bold'})
plt.rcParams.update({'axes.labelsize': font_size})
#plt.rcParams.update({'axes.linewidth': 0.9})
#plt.rcParams.update({'axes.grid': True})
#plt.rcParams.update({'axes.grid.axis': 'both'})
#plt.rcParams.update({'grid.linewidth': 0.7})
#plt.rcParams.update({'grid.color': 'lightgray'})
#plt.rcParams.update({'axes.autolimit_mode': 'round_numbers'})
#plt.rcParams.update({'axes.xmargin': 0})
#plt.rcParams.update({'axes.ymargin': 0 })
plt.rcParams.update({'xtick.labelsize': font_size}) 
#plt.rcParams.update({'xtick.major.width': 0.9})
plt.rcParams.update({'ytick.labelsize': font_size}) 
#plt.rcParams.update({'ytick.major.width': 0.9})
plt.rcParams.update({'legend.fontsize': font_size})
#plt.rcParams.update({'legend.fancybox': True})
#plt.rcParams.update({'lines.linewidth': 1.6})
#plt.rcParams.update({'lines.markersize': 4.0})
#plt.rcParams.update({'figure.figsize': [11.69,8.27]})
#plt.rcParams.update({'figure.subplot.top': 0.90}) # Original value 0.95
#plt.rcParams.update({'figure.subplot.bottom': 0.1}) # Original value 0.05
#plt.rcParams.update({'figure.subplot.left': 0.1}) # Original value 0.06
#plt.rcParams.update({'figure.subplot.right': 0.9}) # Original value 0.96
#plt.rcParams.update({'figure.subplot.hspace': 0.9}) # Original value 0.0
#plt.rcParams.update({'figure.subplot.wspace': 0.9}) # Original value 0.0
#plt.rcParams.update({'savefig.dpi': 150})
#plt.rcParams.update({'savefig.format': 'pdf'})

# Link Python with the Frew COM interface
fr = win32com.client.Dispatch("frewLib.FrewComAuto")

# User input parent directory
input_folder = (
    r"C:\Users\Jack.Taggart\Desktop\Appendix"
    )

        
os.chdir(input_folder)

# List all the Frew models within the parent directory
input_files = []
for file in os.listdir(input_folder):
    if file.endswith(".fwd"):
        input_files.append(file)

# Change current working directory to the one with the input_file in
for file in input_files:
    input_file_path = Path(
            str(
            str(input_folder) + "/" + str(file))
            )
    input_file_name, input_file_extension = os.path.splitext(file)
    
    # Open and clear current results of the working Frew model
    fr.Open(input_file_path)
    fr.DeleteResults()
    
    # Get basic model information
    num_nodes = fr.GetNumNodes()
    num_stages = fr.GetNumStages()
    num_struts = fr.GetNumStruts()
    
    # Get node levels
    node_levels = []
    for node in range(0,num_nodes):
        node_levels.append(fr.GetNodeLevel(node))
    
        
    # Analyse the current model
    fr.Analyse(num_stages)
    
    # Define results dictionary
    results = {}
    
    # Assign the results in the model to the results dictionary
    for stage in range(0,num_stages):
        stage_name = "stage " + str(stage)
        results[stage_name] = {
                "displacements":[],
                "shear":[],
                "bending":[]
                }
        for node in range(0,num_nodes):
            results[stage_name]["displacements"].append(fr.GetNodeDisp(node,stage))
            results[stage_name]["shear"].append(fr.GetNodeShear(node,stage))
            results[stage_name]["bending"].append(fr.GetNodeBending(node,stage))
    
    # Define envelopes dictionary
    envelopes = {
            "maximum":{},
            "minimum":{}
            }
    
    for item in ["maximum","minimum"]:
        envelopes[item] = {
            "displacements":[],
            "shear":[],
            "bending":[]
            }
    
    # Find the maximum value of results for each node and assign it to envelopes
    for node in range(0,num_nodes):
        displacements = []
        shear = []
        bending = []
        
        for stage in range(0,num_stages):
            stage_name = "stage " + str(stage)
            displacements.append(results[stage_name]["displacements"][node])
            shear.append(results[stage_name]["shear"][node])
            bending.append(results[stage_name]["bending"][node])
        
        envelopes["maximum"]["displacements"].append(max(displacements))
        envelopes["maximum"]["shear"].append(max(shear))
        envelopes["maximum"]["bending"].append(max(bending))
        envelopes["minimum"]["displacements"].append(min(displacements))
        envelopes["minimum"]["shear"].append(min(shear))
        envelopes["minimum"]["bending"].append(min(bending))
    
    # Get strut forces
    struts = {}
    for strut in range(0,num_struts):
        struts["strut " + str(strut)] = []
        for stage in range(0,num_stages):
            struts["strut " + str(strut)].append(fr.GetStrutForce(stage,strut))
    
    # Define ground models for left and right hand sides of wall
    LH_soil = {}
    for stage in range(0,num_stages):
        stage_name = "stage " + str(stage)
        LH_soil[stage_name] = []
        for node in range(0,num_nodes):
            LH_soil[stage_name].append(fr.GetSoilZoneLeft(node,stage))
    
    RH_soil = {}
    for stage in range(0,num_stages):
        stage_name = "stage " + str(stage)
        RH_soil[stage_name] = []
        for node in range(0,num_nodes):
            RH_soil[stage_name].append(fr.GetSoilZoneRight(node,stage))
    
    # Get the wall EI profile
    wall_EI = {}
    for stage in range(0,num_stages):
        stage_name = "stage " + str(stage)
        wall_EI[stage_name] = []
        for node in range(0,num_nodes):
            wall_EI[stage_name].append(fr.GetWallEI(node,stage))
    
    # Open pdf for figure export
    pdf = pltexp.PdfPages("%s - results.pdf" %input_file_name)
    
    # Plot the results on figures ready for exporting to a PDF document
    for stage in range(0,num_stages):
        stage_name = "stage " + str(stage)
        figure_name = str(input_file_name) + " - Stage " + str(stage)
        figure = plt.figure()
        plt.clf()
        figure, (ax1, ax2, ax3) = plt.subplots(1,3, gridspec_kw={"width_ratios":[3,3,3]})


        # Sub-plot for displacements
        max_disp = max(results[stage_name]["displacements"])
        ax1.set_xlabel("Displacements (mm)")
        ax1.plot(results[stage_name]["displacements"],node_levels,"b")
        ax1.plot(envelopes["maximum"]["displacements"],node_levels,"k--")
        ax1.plot(envelopes["minimum"]["displacements"],node_levels,"k--")
#        ax1.set_yticklabels([])

        # Plot the maximum point with a label
        max_node = results[stage_name]["displacements"].index(max_disp)
        max_node_level = node_levels[max_node]
        ax1.plot(max_disp, max_node_level, "bo")
        label_x = min(envelopes["minimum"]["displacements"]) + 2.5
        label_y = max(node_levels) + 2.5
        ax1.text(
                0,
                7,
                figure_name)
#        ax1.text(label_x, label_y, "Max displacement: " + str("%.1fmm" %max_disp) +
#                 " at %.1fmGD" %max_node_level)
#        ax1.text(label_x, max(node_levels) + 5, 
#                               "Strut force: %.1fkN" %struts["strut 0"][stage],
#                               fontsize=10)
    
    
        # Sub-plot for shear
        max_shear = max(results[stage_name]["shear"])
        min_shear = min(results[stage_name]["shear"])
        ax2.set_xlabel("Shear (kN)")
        ax2.plot(results[stage_name]["shear"],node_levels,"g")
        ax2.plot(envelopes["maximum"]["shear"],node_levels,"k--")
        ax2.plot(envelopes["minimum"]["shear"],node_levels,"k--")
        ax2.set_yticklabels([])

        # Plot the maximum point with a label
        max_node = results[stage_name]["shear"].index(max_shear)
        max_node_level = node_levels[max_node]
        ax2.plot(max_shear, max_node_level, "go")
        label_x = min(envelopes["minimum"]["shear"]) + 5
        label_y = max(node_levels) + 2.5
#        ax2.text(label_x, label_y, "Max shear: " +
#                     str("%.1fkN" %max_shear) + " at %.1fmGD" %max_node_level)
    
    
        # Sub-plot for bending
        max_bend = max(results[stage_name]["bending"])
        min_bend = min(results[stage_name]["bending"])
        ax3.set_xlabel("Bending Moment (kNm)")
        ax3.plot(results[stage_name]["bending"],node_levels,"r")
        ax3.plot(envelopes["maximum"]["bending"],node_levels,"k--")
        ax3.plot(envelopes["minimum"]["bending"],node_levels,"k--")
        ax3.set_yticklabels([])

        # Plot the maximum point with a label
        max_node = results[stage_name]["bending"].index(max_bend)
        max_node_level = node_levels[max_node]
        ax3.plot(max_bend, max_node_level, "ro")
        label_x = min(envelopes["minimum"]["bending"]) + 150
        label_y = max(node_levels) + 2.5
#        ax3.text(label_x, label_y, "Max moment: " + str("%.1fkNm" %max_bend) +
#                 " at %.1fmGD" %max_node_level)
        
        # Save figure to PDF
        pdf.savefig(figure)
        
        
#        plt.suptitle(str(figure_name))
#        plt.text(0,18,"ARUP",fontsize=25)
        
#        plt.savefig(figure_name + ".pdf")
#        plt.savefig(str(figure_name))
        plt.close("all")
    pdf.close()
fr = None
print("Script run time = %s seconds" % round((time.time()-StartTime),1))





