# coding: utf8
from __future__ import unicode_literals

from spacy.tokens import Doc, Span, Token
from spacy.matcher import PhraseMatcher
#from emoji import UNICODE_EMOJI
from emoticons import BASE_EMOTICONS

from .about import __version__

# make sure multi-character emoji don't contain whitespace


class Emoticon(object):
    """spaCy v2.0 pipeline component for adding emoticons meta data to `Doc` objects.
    Detects text emoticons consisting of one or more text characters into one token. 
    Emoticons are matched using spaCy's `PhraseMatcher`,
    and looked up in the data provided by the "emoticon" package:

    USAGE:
        >>> import spacy
        >>> from spacyemoticons import Emoticon
        >>> nlp = spacy.load('en')
        >>> emoticon = Emoticon(nlp)
        >>> nlp.add_pipe(emoticon, first=True)
        >>> doc = nlp(u"This is a test :) :(")
        >>> assert doc._.has_emoticon == True
    """
    name = 'emoticon'

    def __init__(self, nlp, merge_spans=True, lookup={}, pattern_id='EMOTICON',
                 attrs=('is_emoticon', '_emoticon')):
        """Initialise the pipeline component.

        nlp (Language): The shared nlp object. Used to initialise the matcher
            with the shared `Vocab`, and create `Doc` match patterns.
        attrs (tuple): Attributes to set on the ._ property. Defaults to 'is_emoticon'.
        pattern_id (unicode): ID of match pattern, defaults to 'EMOTICON'. Can be
            changed to avoid ID clashes.
        merge_spans (bool): Merge spans containing multi-character emoticon. Will
            only merge combined emoticon resulting in one icon, not sequences.
        lookup (dict): Optional lookup table that maps emoticon unicode strings
            to custom descriptions, e.g. translations or other annotations.
        RETURNS (callable): A spaCy pipeline component.
        """
        self._is_emoticon, self._emoticon = attrs        
        self.merge_spans = merge_spans
        self.lookup = lookup
        self.matcher = PhraseMatcher(nlp.vocab)
        emoticon_patterns = [nlp(emoticon) for emoticon in BASE_EMOTICONS]
        self.matcher.add(pattern_id, None, *emoticon_patterns)
        # Add attributes
        Doc.set_extension(self._emoticon, getter=self.iter_emoticon)
        Span.set_extension(self._emoticon, getter=self.iter_emoticon)
        Token.set_extension(self._is_emoticon, default=False)


    def __call__(self, doc):
        """Apply the pipeline component to a `Doc` object.

        doc (Doc): The `Doc` returned by the previous pipeline component.
        RETURNS (Doc): The modified `Doc` object.
        """
        matches = self.matcher(doc)
        spans = []  # keep spans here to merge them later
        for _, start, end in matches:
            span = doc[start : end]
            for token in span:
                token._.set(self._is_emoticon, True)
            spans.append(span)
        if self.merge_spans:
            for span in spans:
                span.merge()
        return doc


    def iter_emoticon(self, tokens):
        return [(t.text, 
                 i
                 )
                for i, t in enumerate(tokens)
                if t._.get(self._is_emoticon)]