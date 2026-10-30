// ==========================================
// SMARTCARD JAVASCRIPT
// ==========================================


document.addEventListener(
    "DOMContentLoaded",
    function () {

        initializePasswordToggle();

        initializeFlashMessages();

    }
);


// ==========================================
// SHOW / HIDE PASSWORD
// ==========================================

function initializePasswordToggle() {

    const buttons =
        document.querySelectorAll(
            ".toggle-password"
        );


    buttons.forEach(
        function (button) {

            button.addEventListener(
                "click",
                function () {

                    const targetId =
                        button.getAttribute(
                            "data-target"
                        );


                    const input =
                        document.getElementById(
                            targetId
                        );


                    if (!input) {

                        return;

                    }


                    if (
                        input.type ===
                        "password"
                    ) {

                        input.type = "text";

                        button.textContent =
                            "Hide";

                    } else {

                        input.type =
                            "password";

                        button.textContent =
                            "Show";

                    }

                }
            );

        }
    );

}


// ==========================================
// FLASH MESSAGE
// ==========================================

function initializeFlashMessages() {

    const messages =
        document.querySelectorAll(
            ".alert"
        );


    messages.forEach(
        function (message) {

            setTimeout(
                function () {

                    message.style.opacity =
                        "0";


                    setTimeout(
                        function () {

                            message.remove();

                        },
                        500
                    );

                },
                3000
            );

        }
    );

}


// ==========================================
// COPY CARD URL
// ==========================================

function copyCardUrl() {

    const url =
        window.location.href;


    navigator.clipboard.writeText(url)

        .then(
            function () {

                alert(
                    "Card link copied!"
                );

            }
        )

        .catch(
            function () {

                alert(
                    "Unable to copy card link."
                );

            }
        );

}