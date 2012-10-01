epsilon = 0.001;
buttons_area_xoffset = 0;
buttons_area_yoffset = 0;
buttons_area_x = 0;
buttons_area_y = 0;
button_hole_side = 12; // square holes with rounded corners
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
            circle(r);
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
        botton_holes();
    }
}

module button_holes()
{
    
}

top();
