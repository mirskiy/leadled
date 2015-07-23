jQuery(document).ready(function() {

    $('div').each(function() {
        var th = $(this);
        hex = th.css('backgroundColor');
        rgb = hex.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/);
        var red = rgb[1];
        var green = rgb[2];
        var blue = rgb[3];

		// just the initial setup, set sliders, numbers, bg to value
		// based on bg color from above
        th.find('.r').val(red);
        th.find('.r').parent('span').siblings('input').val(red);
        th.find('.g').val(green);
        th.find('.g').parent('span').siblings('input').val(green);
        th.find('.b').val(blue);
        th.find('.b').parent('span').siblings('input').val(blue);

		// change for any input change, click for any click, keyup for instant text change
		// this was previously $('input').bind, causing it to bind twice
        th.find('input').bind('change keyup click', function() {

			// called once for click, once for change. ok for now
            if ($(this).hasClass('ch')) {		// if we change the slider ('ch') 
                $(this).parent('span').siblings('input').val($(this).val()); // update the numbers
            }

			// called 2 times if we click number (click and change, etc)
            else {  // else we change the number
                if ($(this).val() > 255) $(this).val(255);
                if ($(this).val() < 0) $(this).val(0);
                $(this).siblings('span').find('input').val($(this).val());  // update the slider
            }

			// get color from slider and update #string and bg color
			r = parseInt(th.find('.r').val());
			rHex = r.toString(16);
            if (rHex.length == 1) rHex = '0' + rHex;

            g = parseInt(th.find('.g').val());
			gHex = g.toString(16);
            if (gHex.length == 1) gHex = '0' + gHex;

            b = parseInt(th.find('.b').val());
			bHex = b.toString(16);
            if (bHex.length == 1) bHex = '0' + bHex;

			w = parseInt(th.find('.w').val());

            x = rHex + gHex + bHex;

            th.find('.result').html(x);
            th.css('backgroundColor', '#' + x);

			$.get("/setColor", { red:r, green:g, blue:b, white:w } );

        });

    });

});
