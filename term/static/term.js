var current_command = '';
var current_dir = ''
var ignore_keys = [9,16,17,18,27,37,38,39,40,224];

		
function print(msg){$('#msgbox').append(msg);}
function con(msg){console.log(msg);} 

$(document).ready(function(){
	$('#commandline').focus();
	screen_append('## Starting new session ##');
	$('#screen').focus();
	submit( 'new session' );
});

function screen_append(text){
	var screen_text = $('#screen').val();
	$('#screen').val( screen_text + text );
}

function ps(data,newline,is_command,current_dir){
	if (typeof data == 'string'){
		screen_append(data);
		newline ? screen_append('\n') : {};
	}
	else{			
		for (i=0;i<data.length;i++){
			screen_append(data[i]+'\n');
		}
	}
	if ( ! is_command ){
		screen_append(current_dir+' $  ');
	}
	$('#screen').scrollTop($('#screen')[0].scrollHeight);
}

function submit(submission){
	$.ajax({
		method:'post',
		url:'term.py',
		data:{'package':JSON.stringify(submission)},
		success:function(result){
			result = JSON.parse(result);
			data = result.data;
			current_dir = result.current_dir;
			if (data == 'session started'){
				data = '';
			}
			ps( data=data.trim().split('\n'),newline=null,is_command=false,current_dir=current_dir );
		}
	});
}

$(document).on('keydown','#screen',function(e){
	switch(e.which){
		case 13:
		// Enter
			if (current_command.length == 0){
				ps(data='',newline=true,is_command=false,current_dir=current_dir);
			}
			else{
				submit( current_command );
				ps(data='',newline=true,is_command=true);	
			}
			current_command = '';
			break;
		case 8:
		// Backspace
			if ( current_command.length > 0 ){
				current_command = current_command.substring(0,current_command.length-1);
				var window_text = $('#screen').val();
				$('#screen').val( window_text.substring(0,window_text.length-1) );
			}
			break;
		
		default:
			if ( $.inArray(e.which,ignore_keys) != -1 ){
				return;
			}
			current_command += e.key;
			ps(data=e.key,newline=false,is_command=true);
	}
});