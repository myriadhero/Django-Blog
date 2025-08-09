function cropperWidget() {
    const name = JSON.parse(document.getElementById("cropper-data-name").textContent);
    const cropperWidget = document.getElementById(`cropper-${name}`);
    const previewElem = document.getElementById(`cropper-${name}-preview`);
    const applyButton = document.querySelector(".cropper-widget-apply-button");
    let cropped = false;
    let cropper = previewElem.src ? new Cropper(previewElem, {
        cropend: function () {
            cropped = true;
        },
        zoom: function () {
            cropped = true;
        }
    }) : null;

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

window.addEventListener("DOMContentLoaded", cropperWidget);