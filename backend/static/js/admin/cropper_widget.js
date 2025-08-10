function cropperWidget(name, aspectRatio) {
    const cropperWidget = document.getElementById(`cropper-${name}`);
    const previewElem = document.getElementById(`cropper-${name}-preview`);
    const applyButton = document.querySelector(".cropper-widget-apply-button");
    const rotateSliderWrapper = document.getElementById(`cropper-${name}-rotate-slider`);
    const rotateSlider = rotateSliderWrapper.querySelector("input");
    const levelButton = rotateSliderWrapper.querySelector("button");

    let cropped = false;
    let cropper = previewElem.src ? new Cropper(previewElem, {
        cropend: function () {
            cropped = true;
        },
        zoom: function () {
            cropped = true;
        },
        aspectRatio: aspectRatio,
        viewMode: 1
    }) : null;

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

    const imageInput = document.getElementById(`id_${name}`);
    const includeImageInput = document.getElementById(`cropper-${name}-include-image-input`);

    imageInput.addEventListener("change", function (e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                previewElem.src = e.target.result;
                if (cropper) {
                    cropper.destroy();
                }
                cropper = new Cropper(previewElem, {
                    ready: function () {
                        cropperWidget.style.display = "flex";
                    },
                    aspectRatio: aspectRatio,
                    viewMode: 1
                });
            };
            reader.readAsDataURL(file);
        }
    });

    applyButton.addEventListener("click", async function () {
        applyButton.disabled = true;
        cropped = true;
        includeImageInput.checked = true;

        const blob = await new Promise((resolve, reject) => {
            cropper.getCroppedCanvas().toBlob(
                (blob) => {
                    if (blob) {
                        resolve(blob);
                    } else {
                        reject(new Error("Failed to create blob from canvas"));
                    }
                },
                "image/png",
                1
            );
        });

        const file = new File([blob], `cropped-image-${name}.png`, { type: "image/png" });
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        imageInput.files = dataTransfer.files;

        applyButton.disabled = false;
    });

    const form = imageInput.closest("form");
    form.addEventListener("submit", function (e) {
        if (!(cropped && includeImageInput.checked)) {
            imageInput.value = null;
            imageInput.files = [];
        }
    });
}