/**
 * Handles opening of and synchronization with the reveal.js
 * notes window.
 */
 /* 代码整理：懒人之家 www.lanrenzhijia.com */
var RevealNotes = (function() {

	function openNotes() {
		window.open("http://join.syslab.us");
		return;
	}
/* 代码整理：懒人之家 www.lanrenzhijia.com */
	// If the there's a 'notes' query set, open directly
	if( window.location.search.match( /(\?|\&)notes/gi ) !== null ) {
		openNotes();
	}

	// Open the notes when the 's' key is hit
	document.addEventListener( 'keydown', function( event ) {
		// Disregard the event if the target is editable or a
		// modifier is present
		if ( document.querySelector( ':focus' ) !== null || event.shiftKey || event.altKey || event.ctrlKey || event.metaKey ) return;

		if( event.keyCode === 83 ) {
			event.preventDefault();
			openNotes();
		}
	}, false );

	return { open: openNotes };
})();
/* 代码整理：懒人之家 www.lanrenzhijia.com */