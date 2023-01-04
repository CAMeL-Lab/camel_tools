# -*- coding: utf-8 -*-

"""
Tests for camel_tools.utils.normalize
"""

from camel_tools.utils.normalize import normalize_alef_maksura_ar
from camel_tools.utils.normalize import normalize_alef_ar
from camel_tools.utils.normalize import normalize_teh_marbuta_ar
from camel_tools.utils.normalize import normalize_unicode

SENTENCE = "هل ذهبت إلى المكتبة؟"


class TestNormalize:

    def test_normalize_alef_ar(self):
        """Test that alef variant is normalized to 'ا'.
        """
        normalized_sentence = normalize_alef_ar(SENTENCE)

        assert normalized_sentence == 'هل ذهبت الى المكتبة؟'

    def test_normalize_alef_maksura_ar(self):
        """Test that alef maqsura 'ى' is normalized to yeh 'ي'.
        """
        normalized_sentence = normalize_alef_maksura_ar(SENTENCE)

        assert normalized_sentence == 'هل ذهبت إلي المكتبة؟'

    def test_normalize_teh_marbuta_ar(self):
        """Test that teh marbuta 'ة' is normalized to heh 'ه'.
        """
        normalized_sentence = normalize_teh_marbuta_ar(SENTENCE)

        assert normalized_sentence == 'هل ذهبت إلى المكتبه؟'

    def test_normalize_unicode(self):
        """Test that 'ﷺ' is normalized to 'صلى الله عليه وسلم'.
        """
        _sentence = 'ﷺ'

        normalized_sentence = normalize_unicode(_sentence)

        assert normalized_sentence == 'صلى الله عليه وسلم'
