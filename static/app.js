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