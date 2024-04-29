from .dimension import dimensionlist
from .gropuping import gropuping


def main_draw(self,context):
    layout = self.layout
    seleobj = context.selected_objects
    xlist,ylist,zlist = dimensionlist(self,seleobj)

    #　グループ数の合計を計算　開始
    objlist =[]
    a=0
    for i in seleobj:
        objlist.append({"object":i,"spltname":i.name.split('.', 1)[0]})

    for object, spltname in gropuping(objlist):
          a+=1
    #　グループ数の合計を計算　終了

    layout.prop(self, "only_parent_ojbect_select" )
    layout.prop(self, "look_obname" )
    layout.prop(self, "Determine_the_width_for_each_group" )
    layout.prop(self, "Stacked_on_a_cube" )
    layout.label(text="Dimensition") 
    if  xlist != []:
        layout.label(text="x="+str(max(xlist)))
    if  ylist != []:
        layout.label(text="y="+str(max(ylist)))
    layout.label(text="Total number of groups")
    layout.label(text=str(a) )

    layout.prop(self, "myint" )
    if self.Stacked_on_a_cube == True:
        layout.prop(self, "z_axis_return_number" )
    # layout.label(text="Note: z-axis is not available.")

    layout.prop(self, "Adjustment_of_width_between_groups")
    layout.prop(self, "myfloatvector")
    layout.prop(self, "starting_from_an_active_object" )
    layout.prop(self, "to_origin" )
    ybox = layout.box()
    ybox.prop(self, "yaxisgroupret" )
    ybox.prop(self, "y_axis_direction_to_reverse" )
    ybox.prop(self, "x_axis_direction_to_reverse" )

    if self.Stacked_on_a_cube == False:
        layout.prop(self, "Z_axis_for_line_breaks" )
    elif self.Stacked_on_a_cube == True:
        self.Z_axis_for_line_breaks == False

    layout.prop(self, "gropu_toge" )
    if self.gropu_toge and self.randam_all_gropu==False:
        layout.prop(self, "pass_act_obj" )

    layout.prop(self, "randam_all_gropu" )
    layout.prop(self, "myint2" )

    movebox =layout.box()
    movebox.label(text="Whole Movement") 
    movebox.prop(self, "myfloatvector2")

    transrotatebox =layout.box()
    transrotatebox.prop(self, "tranmormbool" )
    transrotatebox.prop(self, "minustranmormbool" )
    grid = layout.grid_flow(row_major=True, columns=3, even_columns=True, even_rows=True, align=True)
    grid.prop(self, "my_enum",  expand=True )
