const carousel_images = $('#index-carousel').children('img');

if (carousel_images.length > 0) {
  let index = 0;
  window.setInterval(() => {
    const old_index = index;
    const old_image = carousel_images[index];
    do {
      index = (index + 1) % carousel_images.length;
    } while(carousel_images[index].naturalWidth == 0 && index != old_index);
    const new_image = carousel_images[index];
    if (old_image !== new_image) {
      old_image.style.zIndex = 0;
      new_image.style.zIndex = 1;
      $(new_image).addClass('spinning').fadeIn(1500, () => {
	$(new_image).removeClass('spinning');
	$(old_image).hide();
      });
    }
  }, 6000);
}
