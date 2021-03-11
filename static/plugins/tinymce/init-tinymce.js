tinymce.init({
    selector: "#body",
    fontsize_formats: '8px 10px 11px 12px 13px 14px 15px 16px 17px 18px 19px 20px 24px 36px',
    content_style: "@import url('https://fonts.googleapis.com/css2?family=Lato:wght@300&family=Manrope:wght@200&family=Nanum+Gothic&family=Quicksand:wght@300&family=Roboto:wght@300&family=Source+Sans+Pro:wght@300&family=Spartan:wght@300&display=swap');",
    font_formats:
        "Arial Black=arial black,avant garde; Manrope=Manrope;Nanum Gothic=Nanum Gothic;Source Sans Pro Courier=Source Sans Pro;Spartan=Spartan; New=courier new,courier; Lato=Lato; Roboto=Roboto;Quicksand=Quicksand;",
    // plugins: "image,spellchecker,textcolor",
    // toolbar: "undo redo | styleselect | fontselect | fontsizeselect | forecolor backcolor | bold italic | alignleft aligncenter alignright alignjustify | outdent indent",
    theme: 'modern',
    plugins: ['advlist autolink lists link image charmap print preview hr anchor pagebreak',
        'searchreplace wordcount visualblocks visualchars code fullscreen',
        'insertdatetime media nonbreaking save table contextmenu directionality',
        'emoticons template paste textcolor colorpicker spellchecker textpattern imagetools'
    ],
    image_class_list: [
        { title: 'Responsive', value: 'img-responsive' },
        { title: 'None', value: '' }
    ],
    image_caption: true,
    paste_data_images: true,
    image_advtab: true,
    file_picker_callback: function(callback, value, meta) {
      if (meta.filetype == 'image') {
        $('#upload').trigger('click');
        $('#upload').on('change', function() {
          var file = this.files[0];
          var reader = new FileReader();
          reader.onload = function(e) {
            callback(e.target.result, {
              alt: ''
            });
          };
          reader.readAsDataURL(file);
        });
      }
    },
    toolbar1: 'insertfile undo redo | styleselect | fontselect | fontsizeselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link | image',
    toolbar2: 'print preview media | forecolor backcolor emoticons',
    templates: [
        { title: 'Test template 1', content: 'Test 1' },
        { title: 'Test template 2', content: 'Test 2' }
    ],
    setup: function (editor) {
        editor.on('change', function () {
            tinymce.triggerSave();
        });
    }
});


// @import url('https://fonts.googleapis.com/css2?family=Lato:wght@300&family=Manrope:wght@200&family=Nanum+Gothic&family=Quicksand:wght@300&family=Roboto:wght@300&family=Source+Sans+Pro:wght@300&family=Spartan:wght@300&display=swap');
// font-family: 'Lato', sans-serif;

// font-family: 'Manrope', sans-serif;

// font-family: 'Nanum Gothic', sans-serif;

// font-family: 'Quicksand', sans-serif;

// font-family: 'Roboto', sans-serif;

// font-family: 'Source Sans Pro', sans-serif;

// font-family: 'Spartan', sans-serif;