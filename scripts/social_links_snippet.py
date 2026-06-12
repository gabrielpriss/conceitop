"""Links oficiais das redes sociais da Conceito Prime."""

SOCIAL_FACEBOOK = "https://www.facebook.com/ConceitoPrimeSE/"
SOCIAL_INSTAGRAM = "https://www.instagram.com/conceitoprimese/"
SOCIAL_LINKEDIN = "https://www.linkedin.com/company/conceito-prime/"
SOCIAL_YOUTUBE = "https://www.youtube.com/@conceitoprime70"

_SOCIAL_ATTRS = 'target="_blank" rel="noopener noreferrer"'


def render_contact_social_rail():
    return f"""        <aside class="contact-social-rail" aria-label="Redes sociais">
          <a href="{SOCIAL_FACEBOOK}" {_SOCIAL_ATTRS} aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
          <a href="{SOCIAL_INSTAGRAM}" {_SOCIAL_ATTRS} aria-label="Instagram"><i class="fab fa-instagram"></i></a>
          <a href="{SOCIAL_LINKEDIN}" {_SOCIAL_ATTRS} aria-label="LinkedIn"><i class="fab fa-linkedin-in"></i></a>
          <a href="{SOCIAL_YOUTUBE}" {_SOCIAL_ATTRS} aria-label="YouTube"><i class="fab fa-youtube"></i></a>
        </aside>"""


def render_contact_social_mobile():
    return f"""          <div class="contact-social-mobile" aria-label="Redes sociais">
            <a href="{SOCIAL_FACEBOOK}" {_SOCIAL_ATTRS} aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
            <a href="{SOCIAL_INSTAGRAM}" {_SOCIAL_ATTRS} aria-label="Instagram"><i class="fab fa-instagram"></i></a>
            <a href="{SOCIAL_LINKEDIN}" {_SOCIAL_ATTRS} aria-label="LinkedIn"><i class="fab fa-linkedin-in"></i></a>
            <a href="{SOCIAL_YOUTUBE}" {_SOCIAL_ATTRS} aria-label="YouTube"><i class="fab fa-youtube"></i></a>
          </div>"""


def render_footer_social():
    btn = 'class="w-10 h-10 rounded-full border border-white/20 flex items-center justify-center text-white hover:border-gold-400 hover:text-gold-400 transition-all duration-300"'
    return f"""          <div class="flex gap-4">
            <a href="{SOCIAL_FACEBOOK}" {_SOCIAL_ATTRS} {btn} aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
            <a href="{SOCIAL_INSTAGRAM}" {_SOCIAL_ATTRS} {btn} aria-label="Instagram"><i class="fab fa-instagram"></i></a>
            <a href="{SOCIAL_LINKEDIN}" {_SOCIAL_ATTRS} {btn} aria-label="LinkedIn"><i class="fab fa-linkedin-in"></i></a>
            <a href="{SOCIAL_YOUTUBE}" {_SOCIAL_ATTRS} {btn} aria-label="YouTube"><i class="fab fa-youtube"></i></a>
          </div>"""
