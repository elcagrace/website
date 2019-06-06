const MENU_BUTTON_STRING = '<a class="mobile-more" href="#"><span class="mobile-more-line mobile-more-line-0"></span><span class="mobile-more-line mobile-more-line-1"></span><span class="mobile-more-line mobile-more-line-2"></span></a>';

function set_up_mobile_more() {
  const less = $(MENU_BUTTON_STRING);
  const more = $(MENU_BUTTON_STRING);
  $('.menu nav ul li:first-child').prepend(less);
  $('.menu nav ul li.active').prepend(more);
  const collapse = $('.menu nav ul li:not(.active)');

  function update_menu(force_open) {
    if (skel.isActive('mobile')) {
      if (force_open) {
	less.show();
	more.hide();
	collapse.css('height', 'auto');
      } else {
	less.hide();
	more.show();
	collapse.height(0);
      }
    } else {
      less.hide();
      more.hide();
      collapse.css('height', 'auto');
    }
  }

  skel.change(update_menu);
  update_menu(/^http:\/\/egrace.org\/.*$/.test(document.referrer || ''));

  less.on('click', function() {
    less.fadeOut();
    more.fadeIn();
    collapse.animate({ height: 0, });
    return false;
  });

  more.on('click', function() {
    less.fadeIn();
    more.fadeOut();
    for (let i = collapse.length; i-- > 0;) {
      const expanding = $(collapse[i]);
      expanding.css('height', 'auto');
      const height = expanding.height();
      expanding.height(0).animate({ height: height, });
    }
    return false;
  });
}

set_up_mobile_more();
