spacyemoticon: emoticon for spaCy
**************************

`spaCy v2.0 <https://spacy.io/usage/v2>`_ extension and pipeline component
for adding text emoticon meta data to ``Doc`` objects. Detects text emoticons
consisting in one or more characters or symbols into one token. The extension 
sets the custom ``Doc``, ``Token`` and ``Span`` attributes ``._.is_emoticon``,
and ``._.emoticon``. You can read more about custom pipeline
components and extension attributes
`here <https://spacy.io/usage/processing-pipelines>`_.

Emoticon are matched using spaCy's ``PhraseMatcher``, and looked up in the data
table provided by the `"emoticons.py"`_.


⏳ Installation
===============

``spacyemoticon`` requires ``spacy`` v2.0.0 or higher.

.. code:: bash

    pip install spacyemoticon

☝️ Usage
========

Import the component and initialise it with the shared ``nlp`` object (i.e. an
instance of ``Language``), which is used to initialise the ``PhraseMatcher``
with the shared vocab, and create the match patterns. Then add the component
anywhere in your pipeline.

.. code:: python

    import spacy
    from spacyemoticon import Emoticon

    nlp = spacy.load('en')
    emoticon = Emoticon(nlp)
    nlp.add_pipe(emoticon, first=True)

    doc = nlp(u"This is a test :) <\3")
    assert doc[0]._.is_emoticon == False
    assert doc[4]._.is_emoticon == True
    assert len(doc._.emoticon) == 2

``spacyemoticon`` only cares about the token text, so you can use it on a blank
``Language`` instance (it should work for all
`available languages <https://spacy.io/usage/models#languages>`_!), or in
a pipeline with a loaded model. If you're loading a model and your pipeline
includes a tagger, parser and entity recognizer, make sure to add  the emoticon
component as ``first=True``, so the spans are merged right after tokenization,
and *before* the document is parsed. If your text contains a lot of emoticon, this
might even give you a nice boost in parser accuracy.

Available attributes
--------------------

The extension sets attributes on the ``Doc``, ``Span`` and ``Token``. You can
change the attribute names on initialisation of the extension. For more details
on custom components and attributes, see the
`processing pipelines documentation <https://spacy.io/usage/processing-pipelines#custom-components>`_.

====================== ======= ===
``Token._.is_emoticon``   bool    Whether the token is an emoticon.
``Doc._.emoticon``        list    ``(emoticon, index, description)`` tuples of the document's emoticon.
``Span._.emoticon``       list    ``(emoticon, index, description)`` tuples of the span's emoticon.
====================== ======= ===

Settings
--------

On initialisation of ``Emoticon``, you can define the following settings:

=============== ============ ===
``nlp``         ``Language`` The shared ``nlp`` object. Used to initialise the matcher with the shared ``Vocab``, and create ``Doc`` match patterns.
``attrs``       tuple        Attributes to set on the ._ property. Defaults to ``('is_emoticon', 'emoticon')``.
``pattern_id``  unicode      ID of match pattern, defaults to ``'EMOTICON'``. Can be changed to avoid ID conflicts.
``merge_spans`` bool         Merge spans containing multi-character emoticon, defaults to ``True``. Will only merge combined emoticon resulting in one icon, not sequences.
``lookup``      dict         Optional lookup table that maps emoticon text strings to custom descriptions, e.g. translations or other annotations.
=============== ============ ===

.. code:: python

    emoticon = Emoticon(nlp, attrs=('has_e', 'e'), lookup={u':S'})
    nlp.add_pipe(emoticon)
    doc = nlp(u"We can be :S heroes")
    assert doc[3]._.is_e
