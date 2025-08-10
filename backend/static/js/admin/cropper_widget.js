function getMimeTypeFromFileExtension(src) {
    const ext = src.split('.').pop();
    switch (ext) {
        case 'jpg':
        case 'jpeg':
            return 'image/jpeg';
        case 'png':
            return 'image/png';
        default:
            return 'image/png';
    }
}

function cropperWidget(name, aspectRatio) {
    const imageInput = document.getElementById(`id_${name}`);
    const cropperWidget = document.getElementById(`cropper-${name}`);
    const previewElem = cropperWidget.querySelector(`#cropper-${name}-preview`);
    const applyButton = cropperWidget.querySelector(".cropper-widget-button-apply");
    const resetCropButton = cropperWidget.querySelector(".cropper-widget-button-reset-crop");
    const resetFileButton = cropperWidget.querySelector(".cropper-widget-button-reset-file");
    const rotateSliderWrapper = cropperWidget.querySelector(`#cropper-${name}-rotate-slider`);
    const rotateSlider = rotateSliderWrapper.querySelector("input");
    const levelButton = rotateSliderWrapper.querySelector("button");

    const originalSrc = previewElem.getAttribute('src');
    const originalMimeType = originalSrc ? getMimeTypeFromFileExtension(originalSrc) : "image/png";
    let currentMimeType = originalMimeType;

    const cropperOptions = {
        aspectRatio: aspectRatio,
        viewMode: 1,
        minContainerWidth: 300,
        minContainerHeight: 300
    };
    let cropper = previewElem.getAttribute('src') ? new Cropper(previewElem, cropperOptions) : null;

    let prevRotate = 0;
    rotateSlider.addEventListener("input", function (e) {
        cropper?.rotate(e.target.value - prevRotate);
        prevRotate = e.target.value;
    });
    levelButton.addEventListener("click", function () {
        rotateSlider.value = 0;
        cropper?.rotate(-prevRotate);
        prevRotate = 0;
    });

    imageInput.addEventListener("change", function (e) {
        // New image is selected
        const file = e.target.files[0];
        if (file) {
            currentMimeType = getMimeTypeFromFileExtension(file.name);

            const reader = new FileReader();
            reader.onload = function (e) {
                previewElem.setAttribute('src', e.target.result);
                cropper?.destroy();
                cropper = new Cropper(previewElem, {
                    ...cropperOptions,
                    ready: function () {
                        cropperWidget.classList.add("cropper-widget-visible");
                    }
                });
            };
            reader.readAsDataURL(file);
        }
    });

    applyButton.addEventListener("click", async function () {
        // Add image to upload input
        if (!cropper) return;

        applyButton.disabled = true;

        const blob = await new Promise((resolve, reject) => {
            cropper.getCroppedCanvas().toBlob(
                (blob) => {
                    if (blob) {
                        resolve(blob);
                    } else {
                        reject(new Error("Failed to create blob from canvas"));
                    }
                },
                currentMimeType,
                1
            );
        });

        const file = new File([blob], `cropped-image.${currentMimeType.split('/')[1]}`, { type: currentMimeType });
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        imageInput.files = dataTransfer.files;

        applyButton.disabled = false;
    });

    resetCropButton.addEventListener("click", function () {
        cropper?.reset();
        prevRotate = 0;
        rotateSlider.value = 0;
    });

    resetFileButton.addEventListener("click", function () {
        if (!cropper) return;

        // Reset the image input and preview
        // the original here is not the newly uploaded file
        // but the first page load file
        imageInput.value = null;
        imageInput.files = (new DataTransfer()).files;
        previewElem.setAttribute('src', originalSrc);
        currentMimeType = originalMimeType;

        cropper?.destroy();
        cropper = previewElem.getAttribute('src') ? new Cropper(previewElem, cropperOptions) : null;
        prevRotate = 0;
        rotateSlider.value = 0;
        if (originalSrc) {
            cropperWidget.classList.add("cropper-widget-visible");
        } else {
            cropperWidget.classList.remove("cropper-widget-visible");
        }
    });
    
}