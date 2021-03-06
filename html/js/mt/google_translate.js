(function ($) {
  window.PTL.editor.mt = window.PTL.editor.mt || {};

  PTL.editor.mt.google_translate = {

    buttonClassName: "googletranslate",
    imageUri: m("images/google-translate.png"),
    hint: "Google Translate",
    validatePair: false,

    url: "http://ajax.googleapis.com/ajax/services/language/translate",
    pairs: [{"source":"af","target":"af"},
            {"source":"sq","target":"sq"},
            {"source":"ar","target":"ar"},
            {"source":"be","target":"be"},
            {"source":"bg","target":"bg"},
            {"source":"ca","target":"ca"},
            {"source":"zh","target":"zh"},
            {"source":"zh-CN","target":"zh-CN"},
            {"source":"zh-TW","target":"zh-TW"},
            {"source":"hr","target":"hr"},
            {"source":"cs","target":"cs"},
            {"source":"da","target":"da"},
            {"source":"nl","target":"nl"},
            {"source":"en","target":"en"},
            {"source":"et","target":"et"},
            {"source":"tl","target":"tl"},
            {"source":"fi","target":"fi"},
            {"source":"fr","target":"fr"},
            {"source":"gl","target":"gl"},
            {"source":"de","target":"de"},
            {"source":"el","target":"el"},
            {"source":"ht","target":"ht"},
            {"source":"iw","target":"iw"},
            {"source":"hi","target":"hi"},
            {"source":"hu","target":"hu"},
            {"source":"is","target":"is"},
            {"source":"id","target":"id"},
            {"source":"ga","target":"ga"},
            {"source":"it","target":"it"},
            {"source":"ja","target":"ja"},
            {"source":"ko","target":"ko"},
            {"source":"lv","target":"lv"},
            {"source":"lt","target":"lt"},
            {"source":"mk","target":"mk"},
            {"source":"ms","target":"ms"},
            {"source":"mt","target":"mt"},
            {"source":"no","target":"no"},
            {"source":"fa","target":"fa"},
            {"source":"pl","target":"pl"},
            {"source":"pt","target":"pt"},
            {"source":"pt-PT","target":"pt-PT"},
            {"source":"ro","target":"ro"},
            {"source":"ru","target":"ru"},
            {"source":"sr","target":"sr"},
            {"source":"sk","target":"sk"},
            {"source":"sl","target":"sl"},
            {"source":"es","target":"es"},
            {"source":"sw","target":"sw"},
            {"source":"sv","target":"sv"},
            {"source":"tl","target":"tl"},
            {"source":"th","target":"th"},
            {"source":"tr","target":"tr"},
            {"source":"uk","target":"uk"},
            {"source":"vi","target":"vi"},
            {"source":"cy","target":"cy"},
            {"source":"yi","target":"yi"}],

    init: function (apiKey) {
      /* Prepare URL for requests. */
      this.url = PTL.editor.settings.secure == false ? this.url : this.url.replace("http", "https");
      this.url += "?callback=?";
      /* Set target language */
      this.targetLang = PTL.editor.normalizeCode($("div#target_lang").text());
      /* Bind event handler */
      $(".googletranslate").live("click", this.translate);
    },

    ready: function () {
      PTL.editor.addMTButtons(PTL.editor.mt.google_translate);
    },

    translate: function () {
      PTL.editor.translate(this, function(sourceText, langFrom, langTo, resultCallback) {
        var transData = {v: '1.0', q: sourceText,
                         langpair: langFrom + '|' + langTo}
        $.getJSON(PTL.editor.mt.google_translate.url, transData, function (r) {
          if (r.responseData && r.responseStatus == 200) {
            resultCallback(r.responseData.translatedText);
          } else {
            resultCallback(false, "Google Translate Error: " + r.responseDetails);
          }
        });
      });
    }
  };
})(jQuery);
