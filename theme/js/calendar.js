function narrowCalendar() {
  $('.wide-only').hide();
  $('.narrow-only').show();
  $('th.month-header').attr('colspan', '1');
  const tableBody = $('#calendar tbody');
  const days = [];
  tableBody.find('td').each((_, element) => {
    days.push($(element).detach());
  });
  tableBody.empty();
  for (const day of days) {
    const row = $('<tr></tr>');
    day.appendTo(row);
    row.appendTo(tableBody);
    if (!day.children().length) {
      row.hide();
    }
  }
}

function widenCalendar() {
  $('.narrow-only').hide();
  $('.wide-only').show();
  $('th.month-header').attr('colspan', '7');
  const tableBody = $('#calendar tbody');
  const days = [];
  tableBody.find('td').each((_, element) => {
    days.push($(element).detach());
  });
  tableBody.empty();
  let fill = 0;
  let row = undefined;
  for (const day of days) {
    if (fill % 7 === 0) {
      if (row !== undefined) {
	row.appendTo(tableBody);
      }
      row = $('<tr></tr>');
    }
    day.appendTo(row);
    day.show();
    ++fill;
  }
  if (row !== undefined) {
    row.appendTo(tableBody);
  }
}

function collapseEvent() {
  $('div.expanded-event').hide();
}

function expandEvent(uuid) {
  $('div.expanded-event').hide();
  const expansion = $(`div.expanded-event[uuid="${uuid}"]`);
  window.setTimeout(() => {
    const bodyOuterWidth = $(document.body).outerWidth();
    const link = $(`li[uuid="${uuid}"] a`);
    let shift = 0;
    if (bodyOuterWidth > 500) { // 500 from CSS
      const targetShift = link.offset().left + link.width() / 2 - bodyOuterWidth / 2;
      const shiftLimit = (bodyOuterWidth - 500) / 2; // 500 from CSS
      shift = Math.max(Math.min(targetShift, shiftLimit), -shiftLimit);
      console.log(targetShift, shiftLimit, shift);
    }
    expansion.css({
      'left': 0,
      'top': link.offset().top + 32,
    });
    expansion.children().css({
      'margin-left': shift > 0 ? 2 * shift : 0,
      'margin-right': shift < 0 ? -2 * shift : 0,
    });
    expansion.show();
  }, 100);
}

function respond() {
  if (skel.isActive('mobile')) {
    narrowCalendar();
  } else {
    widenCalendar();
  }
  const openExpansion = $('div.expanded-event:visible');
  if (openExpansion.length) {
    expandEvent(openExpansion.attr('uuid'));
  }
}
skel.change(respond);
respond();

function move_to_anchor() {
  $('.highlight').removeClass('highlight');
  if (!document.location.hash.substring(1)) {
    return;
  }
  const item = $(`#${document.location.hash.substring(1)}`);
  if (!item.length || !item.is('li')) {
    return;
  }
  item.addClass('highlight');
  const body = $('html,body');
  body.scrollTop(item.offset().top - body.offset().top + body.scrollTop());
  const click_target = item.find('a');
  if (click_target !== undefined) {
    click_target.trigger('click');
  }
}
$(window).on('hashchange', move_to_anchor);
move_to_anchor();
