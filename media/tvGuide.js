/*
The following function is a plug-in by Allan Jardine
(http://www.sprymedia.co.uk/)
It was slightly modified so that when a table is reloaded using
this function the tvGuide table was scanned again to
highlight the user's favourites. 
Code acquired from: http://www.datatables.net/plug-ins/api
*/
$.fn.dataTableExt.oApi.fnReloadAjax = function ( oSettings, sNewSource, fnCallback, bStandingRedraw ){
	if ( typeof sNewSource != 'undefined' && sNewSource != null ){
		oSettings.sAjaxSource = sNewSource;
	}
	this.oApi._fnProcessingDisplay( oSettings, true );
	var that = this;
	var iStart = oSettings._iDisplayStart;
	
	oSettings.fnServerData( oSettings.sAjaxSource, null, function(json) {
		/* Clear the old information from the table */
		that.oApi._fnClearTable( oSettings );
		
		/* Got the data - add it to the table */
		for ( var i=0 ; i<json.aaData.length ; i++ )
		{
			that.oApi._fnAddData( oSettings, json.aaData[i] );
		}
		
		oSettings.aiDisplay = oSettings.aiDisplayMaster.slice();
		that.fnDraw( that );
		
		if ( typeof bStandingRedraw != 'undefined' && bStandingRedraw === true )
		{
			oSettings._iDisplayStart = iStart;
			that.fnDraw( false );
		}
		
		that.oApi._fnProcessingDisplay( oSettings, false );
		
		/* Callback user function - for event handlers etc */
		if ( typeof fnCallback == 'function' && fnCallback != null )
		{
			fnCallback( oSettings );
		}
		checktable(); //Added to make favourites highlighted whenever the table is reloaded.
	} );
	
}

/*returns the selected row(s) of a table*/
function fnGetSelected( oTableLocal ){
	var aReturn = new Array();
	var aTrs = oTableLocal.fnGetNodes();
	
	for ( var i=0 ; i<aTrs.length ; i++ )
	{
		if ( $(aTrs[i]).hasClass('row_selected') )
		{
			aReturn.push( aTrs[i] );
		}
	}
	return aReturn;
}

/*This function scans the tv Guide table and 'highlights' 
any that are the user's favourite*/
function checktable(){
	for(var i=0; i < theguide.fnGetData().length; i++){
		var aData = theguide.fnGetData( i );
		var sID = aData[0];
		var highlight = false;
		for(x=0;x<favs.fnGetData().length; x++){
			var aData_fav = favs.fnGetData( x );
			var sID_fav = aData_fav[0];
			if ( sID == sID_fav ){
				highlight = true;
			}
		}
		var the_node = theguide.fnGetNodes(i);
		if (highlight){
			$(the_node).css("font-weight","bold");
			$(the_node).css("color", "red");
		}else{
			$(the_node).css("font-weight","normal");
			$(the_node).css("color", "black");
		}
	}
}

$(document).ready(function() {
	//add date picker object
	$('#datepicker').datepicker({
		onSelect: function(date) {
			var year = $('#datepicker').datepicker("getDate").getFullYear();
			var month  = $('#datepicker').datepicker("getDate").getMonth()+1;
			var day  = $('#datepicker').datepicker("getDate").getDate();
			theguide.fnSettings().sAjaxSource = "tvjson/"+year+"/"+month+"/"+day;
			theguide.fnReloadAjax();

		},
		inline: true
	}); //end of date picker
	
	//create the DataTable for the tv Guide
	theguide = $('#guide').dataTable( {
		"bProcessing": true,
		"aaSorting": [[ 1, "asc" ]],
		"iDisplayLength": 50,
		"oLanguage": {
			"sEmptyTable": "No shows available for the selected date"
		},
		"aoColumns"   : [{ "bSearchable": true, "bVisible": false }, null, null, null],
		"sAjaxSource": "tvjson/" + $('#datepicker').datepicker("getDate").getFullYear()+"/"+($('#datepicker').datepicker("getDate").getMonth()+1)+"/"+$('#datepicker').datepicker("getDate").getDate(),
		"fnInitComplete": function() {
			checktable();
		}
	} ); //end of tv Guide table
	
	//create the DataTable for the favourites list
	favs = $('#favs').dataTable( {
		"aoColumns"   : [ { "bSearchable": true, "bVisible": false }, null],
		"sAjaxSource": "favShowList/",
		"oLanguage": {
			"sEmptyTable": "No favourites are selected"
		},
		"fnInitComplete": function() {
			checktable();
		}
	} ); //end of favourites table
	
	/*add action handler: for clicking tv Guide table*/
	$("#guide tbody").click(function(event) {
		var iPos = theguide.fnGetPosition( event.target.parentNode );
		var aData = theguide.fnGetData( iPos );
		if( aData != null){
			var show_id = aData[0];
			$.post("toggleFavShow/"+show_id,
			   function(data){
				 favs.fnReloadAjax();
			  });
		}

	});
	/*add action handler: for clicking favourites table*/
	$("#favs tbody").click(function(event) {
		$(favs.fnSettings().aoData).each(function (){
			$(this.nTr).removeClass('row_selected');
		});
		$(event.target.parentNode).addClass('row_selected');
	});
	/*add action handler: for clicking delete button for favourites*/
	$('#delete').click( function() {
		var anSelected = fnGetSelected( favs );
		if (anSelected.length != 0){
			var aData = favs.fnGetData(anSelected[0]);
			var show_id = aData[0];
			$.post("toggleFavShow/"+show_id,
			   function(data){
				 favs.fnReloadAjax();
			  });
		 }
	});
}); //end of document.ready()