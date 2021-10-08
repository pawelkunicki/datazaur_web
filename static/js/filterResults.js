
var search_box = document.getElementById('search_box');
var table = document.getElementsByTagName('table')[0];


search_box.addEventListener('keyup', function (){
	let filtered_table = table;
	let text = this.text;
	console.log(text);
	if (!text){
		for (row of table.rows){
			$(row).show();
		}
	}
	 else {
		for (row of table.rows){
			if ($(row).parent().is('thead')){
				continue;
			}
			else if (row.cells[1].innerHTML.toLowerCase().includes(text.toLowerCase())){
				$(row).show();
				}
            else if (row.cells[2].innerHTML.toLowerCase().includes(text.toLowerCase())){
				$(row).show();
			    }
			else {
				$(row).hide();
				}
			};
		};
		};
	);


