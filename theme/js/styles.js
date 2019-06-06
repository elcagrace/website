skel.init({
    'reset': 'normalize',
    'breakpoints': {
	'mobile': {
	    media: '(max-width: 800px)',
	    href: '/css/style-mobile.css',
	    containers: '100%!',
	    grid: {
		zoom: 3,
		gutters: ['10px', '10px'], // vertical, horizontal
	    },
	},
	'desktop-small': {
	    media: '(min-width: 801px) and (max-width: 1000px)',
	    href: './theme/css/style-desktop.css',
	    containers: '800px!',
	    grid: {
		zoom: 1,
	    },
	},
	'desktop-medium': {
	    media: '(min-width: 1001px) and (max-width: 1200px)',
	    href: './theme/css/style-desktop.css',
	    containers: '1000px!',
	    grid: {
		zoom: 1,
	    },
	},
	'desktop-big': {
	    media: '(min-width: 1201px)',
	    href: './theme/css/style-desktop.css',
	    containers: '1200px!',
	    grid: {
		zoom: 1,
	    },
	},
    },
});
