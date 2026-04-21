def get_css():
    return """
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; border: 1px solid #30363D; }
    [data-testid="stSidebar"] { background-color: #161B22; border-right: 1px solid #30363D; }
    .stChatInputContainer { padding-bottom: 20px; }
    
    /* Фикс для мобильных */
    @media (max-width: 640px) {
        .stChatMessage { font-size: 14px; padding: 10px; }
        .main .block-container { padding-top: 1rem; }
    }
    </style>
    """

PWA_JS = """
<script>
// Авто-скролл вниз при новом сообщении
const observer = new MutationObserver(() => {
    window.scrollTo(0, document.body.scrollHeight);
});
observer.observe(document.body, {childList: true, subtree: true});
</script>
"""
