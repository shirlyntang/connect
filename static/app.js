function readURL(input) {
  	if (input.files && input.files[0]) {
		var reader = new FileReader();

        reader.onload = function (e) {
            $('#image_upload_preview').attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }
}

$("#pic").change(function () {
    readURL(this);
});

function contact() {
	var hideDiv = document.getElementById("toHide");
	hideDiv.style.display = "none";
	var showDiv = document.getElementById("toShow");
	showDiv.style.display = "block";
}