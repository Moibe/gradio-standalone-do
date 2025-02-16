css = """
#warning {background-color: #FFCCCB}
.feedback textarea {font-size: 24px !important}
footer {visibility: hidden}
.gradio-container1{
    /* background-image: linear-gradient(-45deg, #FF66CC, #e73c7e, #23a6d5, #FFA500); */
    background-image: linear-gradient(-45deg, #f77fcf, #e97da6, #74bdd8, #f7ecd8);
    background-size: 400% 400%;
    animation: gradient 15s ease infinite;
    height: 100%;
    width: 100%;
}

.container1 {
    /* padding: 30px;
    height: 315px; */    
    /* background: rgba(125, 249, 255, 0.2);     */
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    background-image: linear-gradient(-45deg, #f77fcf, #e97da6, #74bdd8, #f7ecd8);
    /* background-size: 400% 400%; */
    animation: gradient 15s ease infinite;
    /* backdrop-filter: blur(7px);
    -webkit-backdrop-filter: blur(7px); */
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.18);
}


@keyframes gradient {
    0% {
        background-position: 0% 50%;
    }

    50% {
        background-position: 100% 50%;
    }

    100% {
        background-position: 0% 50%;
    }
}

.animate__animated {
    -webkit-animation-duration: 1s;
    animation-duration: 1s;
    -webkit-animation-duration: var(--animate-duration);
    animation-duration: var(--animate-duration);
    -webkit-animation-fill-mode: both;
    animation-fill-mode: both
}



.button__text {
    background: #3867d6;
    color: #fff;
    padding: 1em 3em;
    border-radius: 3em;
    font: 600 1rem/1 "Lato", sans-serif;
    white-space: nowrap;
    position: relative;
    z-index: 1;
    letter-spacing: 0.075em;
    border: 3px solid transparent;
    text-transform: uppercase;
}
"""