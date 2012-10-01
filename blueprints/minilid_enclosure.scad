epsilon = 0.001;
buttons_area_xoffset = 52;
buttons_area_yoffset = 10;
buttons_area_x = 0;
buttons_area_y = 0;
button_hole_side = 12; // square holes with rounded corners
button_hole_r = 2;
button_distance = 20; // Center-to-center

pcb_x = 20*10;
pcb_y = 15*10;
main_x = pcb_x+10; // 5mm over both sides
main_y = pcb_y+10;

// Helper
module roundedsq(x,y,r)
{
    $fa=0.1;
    $fs=0.05;
    translate([r,r,0])
    {
        minkowski()
        {
            square([x-r,y-r]);
            circle(r, center=true);
        }
    }
}

module button_holes()
{
    translate([buttons_area_xoffset, buttons_area_yoffset,0])
    {
        for(xi=[0:6])
        {
            for(yi=[0:6])
            {
                translate([xi*button_distance, yi*button_distance, 0])
                {
                    translate([1,1,0])
                    {
                        %square(button_distance-2);
                    }
                    translate([button_hole_side/4, button_hole_side/4, 0])
                    {
                        roundedsq(button_hole_side, button_hole_side, button_hole_r);
                    }
                }
            }
        }
    }
}


module bottom()
{
    roundedsq(main_x, main_y, 5);
}

module top()
{
    difference()
    {
        roundedsq(main_x, main_y, 5);
        button_holes();
    }
}


//button_holes();
top();
