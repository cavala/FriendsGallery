/**
 * Image preset
 * If the input file is too large, MAX_WIDTH and MAX_HEIGHT will ensure that its content has small size
 *
 */
const MAX_WIDTH = 1024;
const MAX_HEIGHT = 768;
const QUALITY = { low: 0.2, medium: 0.5, full: 1 };
let app = new Vue({
    el: "#app",
    data: {
        content: 'Vue image preview',
        images: new Array(3)
            .fill()
            .map((el, index) => ({ content: null, key: index })),
        dragEnter: false        
    },
    return: {
        comment:''        
    },
    methods: {
        submitPost(){
            this.comment.push()
        },
        onImage(index, e, method) {
            e.stopPropagation();
            e.preventDefault();
            if (index === 2) this.dragEnter = false;
            // check if it's a drop or upload event.
            const file = e.dataTransfer ? e.dataTransfer.files[0] : e.target.files[0];
            if (!file.type.match('image.*')) alert('Select a valid image file');
            // file is too large (more than 1 MB)
            else if (file.size > 1e6) this.resizeImage(index, file, method);
            else this.images[index].content = URL.createObjectURL(file);
        },
        removeImage(index) {
            this.dragEnter = false;
            this.images[index].content = null;
        },
        resizeImage(index, file, method) {
            const reader = new FileReader();
            reader.onload = readerEvent => {
                const img = new Image();
                // Start the image resizing process
                img.onload = () => {
                    const { width, height } =
                        method === 1
                            ? this.aspectRatioResize(300)
                            : this.proportionalResize(img.width, img.height);
                    const canvas = document.createElement('canvas');
                    canvas.width = width;
                    canvas.height = height;
                    // that's used to draw graphics on the canvas by specifying the position, width and height of the image.
                    canvas.getContext('2d').drawImage(img, 0, 0, width, height);
                    // Export the canvas as a blob (base64) or DataURL by specifying MIME type, image quality
                    this.images[index].content = canvas.toDataURL(
                        'image/jpeg',
                        QUALITY.medium
                    );
                };
                img.src = readerEvent.target.result;
            };
            // Read the input image using FileReader (this fires the reader.onload event).
            reader.readAsDataURL(file);
        },
        aspectRatioResize(length) {
            const aspectRatio = Math.round(screen.width / screen.height);
            return {
                width: length / Math.sqrt(1 / Math.pow(aspectRatio, 2) + 1),
                height: length / Math.sqrt(Math.pow(aspectRatio, 2) + 1)
            };
        },
        proportionalResize(width, height) {
            return {
                width: Math.round((MAX_WIDTH / width) * width),
                height: Math.round((MAX_HEIGHT / height) * height)
            };
        },
        submit : function(){
               this.$refs.form.submit()
        }
    }
});
