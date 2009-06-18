#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Zuza Software Foundation
#
# This file is part of Pootle.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'pootle.settings'

from django.db import transaction

from django.core.management.base import NoArgsCommand
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        create_default_db()

def create_default_db():
    """This creates the default database to get a working Pootle installation.

    You can tweak the methods called or their implementation elsewhere in the
    file. This provides some sane default to get things working."""
    try:
        try:
            transaction.enter_transaction_management()
            transaction.managed(True)

            create_misc()
            create_default_projects()
            create_default_languages()
            create_default_users()
            create_pootle_permissions()
            create_pootle_permission_sets()
        except:
            if transaction.is_dirty():
                transaction.rollback()
            transaction.leave_transaction_management()
            raise
    finally:
        if transaction.is_managed():
            if transaction.is_dirty():
                transaction.commit()
            transaction.leave_transaction_management()

def create_misc():
    """Create miscellaneous database items."""
    from pootle_app.models import Directory
    directory = Directory(name='')
    directory.save()

def create_pootle_permissions():
    """Create default permissions for Pootle."""
    pootle_content_type = ContentType(name="pootle", app_label="pootle_app", model="")
    pootle_content_type.save()
    view = Permission(name="Can view a translation project", content_type=pootle_content_type, codename="view")
    view.save()
    suggest = Permission(name="Can make a suggestion for a translation", content_type=pootle_content_type, codename="suggest")
    suggest.save()
    translate = Permission(name="Can submit a translation", content_type=pootle_content_type, codename="translate")
    translate.save()
    overwrite = Permission(name="Can overwrite translations on uploading files", content_type=pootle_content_type, codename="overwrite")
    overwrite.save()
    review = Permission(name="Can review translations", content_type=pootle_content_type, codename="review")
    review.save()
    archive = Permission(name="Can download archives of translation projects", content_type=pootle_content_type, codename="archive")
    archive.save()
    compile_po_files = Permission(name="Can compile translation files to MO files", content_type=pootle_content_type, codename="compile_po_files")
    compile_po_files.save()
    assign = Permission(name="Can assign work to users", content_type=pootle_content_type, codename="assign")
    assign.save()
    administrate = Permission(name="Can administrate a translation project", content_type=pootle_content_type, codename="administrate")
    administrate.save()
    commit = Permission(name="Can commit to version control", content_type=pootle_content_type, codename="commit")
    commit.save()

def create_pootle_permission_sets():
    """Create the default permission set for the anonymous (non-logged in) user
    ('nobody') and for the logged in user ('default')."""
    from pootle_app.models.permissions import PermissionSet, get_pootle_permission
    from pootle_app.models import Directory
    from pootle_app.models.profile import PootleProfile

    root = Directory.objects.root
    #permissions for the 'nobody' user: view only
    profile = PootleProfile.objects.select_related(depth=1).get(user__username='nobody')
    permission_set = PermissionSet(profile=profile, directory=root)
    permission_set.save()
    permission_set.positive_permissions = [get_pootle_permission('view')]
    permission_set.save()
    #permissions for the 'default' user: view, suggest
    profile = PootleProfile.objects.select_related(depth=1).get(user__username='default')
    permission_set = PermissionSet(profile=profile, directory=root)
    permission_set.save()
    permission_set.positive_permissions = [get_pootle_permission('view'), get_pootle_permission('suggest')]
    permission_set.save()

def create_default_projects():
    """Create the default projects that we host. You might want to add your
    projects here, although you can also add things through the web interface
    later."""
    from pootle_app.models import Project

    pootle = Project(code=u"pootle")
    pootle.fullname = u"Pootle"
    pootle.description = "<div dir='ltr' lang='en'>Interface translations for Pootle. <br /> See the <a href='http://pootle.locamotion.org'>official Pootle server</a> for the translations of Pootle.</div>"
    pootle.checkstyle = "standard"
    pootle.localfiletype = "po"
    pootle.treestyle = "auto"
    pootle.save()

    terminology = Project(code=u"terminology")
    terminology.fullname = u"Terminology"
    terminology.description = "<div dir='ltr' lang='en'>Terminology project that Pootle should use to suggest terms.<br />There might be useful terminology files on the <a href='http://pootle.locamotion.org/projects/terminology/'>official Pootle server</a>.</div>"
    terminology.checkstyle = "standard"
    terminology.localfiletype = "po"
    terminology.treestyle = "auto"
    terminology.save()

    tutorial = Project(code=u"tutorial")
    tutorial.fullname = u"Tutorial"
    tutorial.description = "<div dir='ltr' lang='en'>Tutorial project where users can play with Pootle and learn more about translation and localisation.<br />For more help on localisation, visit the <a href='http://translate.sourceforge.net/wiki/guide/start'>localisation guide</a>.</div>"
    tutorial.checkstyle = "standard"
    tutorial.localfiletype = "po"
    tutorial.treestyle = "auto"
    tutorial.save()

def create_default_languages():
    """Create the default languages. We afford this priviledge to languages
    with reasonably complete interface translations for Pootle."""
    from pootle_app.models import Language

    af = Language(code="af")
    af.fullname = u"Afrikaans"
    af.specialchars = u"ëïêôûáéíóúý"
    af.nplurals = '2'
    af.pluralequation = "(n != 1)"
    af.save()

# Akan
#    ak.fullname = u'Akan'
#    ak.pluralequation = u'(n > 1)'
#    ak.specialchars = "ɛɔƐƆ"
#    ak.nplurals = u'2'

# العربية
# Arabic
    ar = Language(code="ar")
    ar.fullname = u'Arabic'
    ar.nplurals = '6'
    ar.pluralequation = 'n==0 ? 0 : n==1 ? 1 : n==2 ? 2 : n%100>=3 && n%100<=10 ? 3 : n%100>=11 && n%100<=99 ? 4 : 5'
    ar.save()

# Azərbaycan
# Azerbaijani
#    az.fullname = u'Azerbaijani'
#    az.nplurals = '2'
#    az.pluralequation = '(n != 1)'

# Беларуская
# Belarusian
#    be.fullname = u'Belarusian'
#    be.nplurals = '3'
#    be.pluralequation = '(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2)'

# Български
# Bulgarian
#    bg.fullname = u'Bulgarian'
#    bg.nplurals = '2'
#    bg.pluralequation = '(n != 1)'

# বাংলা
# Bengali
#    bn.fullname = u'Bengali'
#    bn.nplurals = '2'
#    bn.pluralequation = '(n != 1)'

# Bengali (India)
#    bn.fullname = u'Bengali (India)'
#    bn.nplurals = '2'
#    bn.pluralequation = '(n != 1)'

# Tibetan
#    bo.fullname = u'Tibetan'
#    bo.nplurals = '1'
#    bo.pluralequation = '0'

# Bosanski
# Bosnian
#    bs.fullname = u'Bosnian'
#    bs.nplurals = '3'
#    bs.pluralequation = '(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2)'

# Català
# Catalan
    ca = Language(code="ca")
    ca.fullname = u'Catalan; Valencian'
    ca.nplurals = '2'
    ca.pluralequation = '(n != 1)'
    ca.save()

# Česky
# Czech
    cs = Language(code="cs")
    cs.fullname = u'Czech'
    cs.nplurals = '3'
    cs.pluralequation = '(n==1) ? 0 : (n>=2 && n<=4) ? 1 : 2'
    cs.save()

# Cymraeg
# Welsh
#    cy.fullname = u'Welsh'
#    cy.nplurals = '2'
#    cy.pluralequation = '(n==2) ? 1 : 0'

# Dansk
# Danish
    da = Language(code="da")
    da.fullname = u'Danish'
    da.nplurals = '2'
    da.pluralequation = '(n != 1)'
    da.save()

# Deutsch
# German
    de = Language(code="de")
    de.fullname = u'German'
    de.nplurals = '2'
    de.pluralequation = '(n != 1)'
    de.save()

# ང་ཁ
# Dzongkha
#    dz.fullname = u'Dzongkha'
#    dz.nplurals = '1'
#    dz.pluralequation = '0'

# Ελληνικά
# Greek
    el = Language(code="el")
    el.fullname = u'Greek'
    el.nplurals = '2'
    el.pluralequation = '(n != 1)'
    el.save()

# English
    en = Language(code="en")
    en.fullname = u'English'
    en.nplurals = '2'
    en.pluralequation = '(n != 1)'
    en.save()

# English (United Kingdom)
    en_GB = Language(code="en_GB")
    en_GB.fullname = u'English (United Kingdom)'
    en_GB.nplurals = '2'
    en_GB.pluralequation = '(n != 1)'
    en_GB.save()

# English (South Africa)
    en_ZA = Language(code="en_ZA")
    en_ZA.fullname = u'English (South Africa)'
    en_ZA.nplurals = '2'
    en_ZA.pluralequation = '(n != 1)'
    en_ZA.save()

# Esperanto
#    eo.fullname = u'Esperanto'
#    eo.nplurals = '2'
#    eo.pluralequation = '(n != 1)'

# Español
# Spanish
    es = Language(code="es")
    es.fullname = u'Spanish; Castilian'
    es.nplurals = '2'
    es.pluralequation = '(n != 1)'
    es.save()

# Español
# Spanish (Argentina)
#    es_AR = Language(code="es_AR")
#    es_AR.fullname = u'Spanish; Castilian (Argentina)'
#    es_AR.nplurals = '2'
#    es_AR.pluralequation = '(n != 1)'
#    es_AR.save()

# Eesti
# Estonian
#    et.fullname = u'Estonian'
#    et.nplurals = '2'
#    et.pluralequation = '(n != 1)'

# Euskara
# Basque
    eu = Language(code="eu")
    eu.fullname = u'Basque'
    eu.nplurals = '2'
    eu.pluralequation = '(n != 1)'
    eu.save()

# فارسی
# Persian
    fa = Language(code="fa")
    fa.fullname = u'Persian'
    fa.nplurals = '1'
    fa.pluralequation = '0'
    fa.save()

# Suomi
# Finnish
    fi = Language(code="fi")
    fi.fullname = u'Finnish'
    fi.nplurals = '2'
    fi.pluralequation = '(n != 1)'
    fi.save()

# Føroyskt
# Faroese
#    fo.fullname = u'Faroese'
#    fo.nplurals = '2'
#    fo.pluralequation = '(n != 1)'

# Français
# French
    fr = Language(code="fr")
    fr.fullname = u'French'
    fr.nplurals = '2'
    fr.pluralequation = '(n > 1)'
    fr.save()

# Furlan
# Friulian
    fur = Language(code="fur")
    fur.fullname = u'Friulian'
    fur.nplurals = '2'
    fur.pluralequation = '(n != 1)'
    fur.save()

# Frysk
# Frisian
    fy = Language(code="fy")
    fy.fullname = u'Western Frisian'
    fy.nplurals = '2'
    fy.pluralequation = '(n != 1)'
    fy.save()

# Gaeilge
# Irish
    ga = Language(code="ga")
    ga.fullname = u'Irish'
    ga.nplurals = '3'
    ga.pluralequation = 'n==1 ? 0 : n==2 ? 1 : 2'
    ga.save()

# Galego
# Galician
    gl = Language(code="gl")
    gl.fullname = u'Galician'
    gl.nplurals = '2'
    gl.pluralequation = '(n != 1)'
    gl.save()

# ગુજરાતી
# Gujarati
#    gu.fullname = u'Gujarati'
#    gu.nplurals = '2'
#    gu.pluralequation = '(n != 1)'

# עברית
# Hebrew
    he = Language(code="he")
    he.fullname = u'Hebrew'
    he.nplurals = '2'
    he.pluralequation = '(n != 1)'
    he.save()

# हिन्दी
# Hindi
#    hi.fullname = u'Hindi'
#    hi.nplurals = '2'
#    hi.pluralequation = '(n != 1)'

# Hrvatski
# Croatian
#    hr.fullname = u'Croatian'
#    hr.nplurals = '3'
#    hr.pluralequation = '(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2)'

# Haitian Creole
    ht = Language(code="ht")
    ht.fullname = u'Haitian; Haitian Creole'
    ht.nplurals = '2'
    ht.pluralequation = '(n !=1)'
    ht.save()

# Magyar
# Hungarian
    hu = Language(code="hu")
    hu.fullname = u'Hungarian'
    hu.nplurals = '2'
    hu.pluralequation = '(n !=1)'
    hu.save()

# Bahasa Indonesia
# Indonesian
    id = Language(code="id")
    id.fullname = u'Indonesian'
    id.nplurals = '1'
    id.pluralequation = '0'
    id.save()

# Icelandic
    islang = Language(code="is")
    islang.fullname = u'Icelandic'
    islang.nplurals = '2'
    islang.pluralequation = '(n != 1)'
    islang.save()

# Italiano
# Italian
    it = Language(code="it")
    it.fullname = u'Italian'
    it.nplurals = '2'
    it.pluralequation = '(n != 1)'
    it.save()

# 日本語
# Japanese
    ja = Language(code="ja")
    ja.fullname = u'Japanese'
    ja.nplurals = '1'
    ja.pluralequation = '0'
    ja.save()

# ქართული
# Georgian
    ka = Language(code="ka")
    ka.fullname = u'Georgian'
    ka.nplurals = '1'
    ka.pluralequation = '0'
    ka.save()

# ភាសា
# Khmer
#    km.fullname = u'Khmer'
#    km.nplurals = '1'
#    km.pluralequation = '0'

# 한국어
# Korean
    ko = Language(code="ko")
    ko.fullname = u'Korean'
    ko.nplurals = '1'
    ko.pluralequation = '0'
    ko.save()

# Kurdî / كوردي
# Kurdish
    ku = Language(code="ku")
    ku.fullname = u'Kurdish'
    ku.nplurals = '2'
    ku.pluralequation = '(n != 1)'
    ku.save()

# Lëtzebuergesch
# Letzeburgesch
#    lb.fullname = u'Letzeburgesch'
#    lb.nplurals = '2'
#    lb.pluralequation = '(n != 1)'

# Lietuvių
# Lithuanian
    lt = Language(code="lt")
    lt.fullname = u'Lithuanian'
    lt.nplurals = '3'
    lt.pluralequation = '(n%10==1 && n%100!=11 ? 0 : n%10>=2 && (n%100<10 || n%100>=20) ? 1 : 2)'
    lt.save()

# Latviešu
# Latvian
#    lv.fullname = u'Latvian'
#    lv.nplurals = '3'
#    lv.pluralequation = '(n%10==1 && n%100!=11 ? 0 : n != 0 ? 1 : 2)'

# Malayalam
    ml = Language(code="ml")
    ml.fullname = u'Malayalam'
    ml.nplurals = '2'
    ml.pluralequation = '(n != 1)'
    ml.save()

# Malagasy
#    mg.fullname = u'Malagasy'
#    mg.nplurals = '2'
#    mg.pluralequation = '(n > 1)'

# Монгол
# Mongolian
    mn = Language(code="mn")
    mn.fullname = u'Mongolian'
    mn.nplurals = '2'
    mn.pluralequation = '(n != 1)'
    mn.save()

# Marathi
#    mr.fullname = u'Marathi'
#    mr.nplurals = u'2'
#    mr.pluralequation = u'(n != 1)'

# Malay
#    ms.fullname = u'Malay'
#    ms.nplurals = u'1'
#    ms.pluralequation = u'0'

# Malti
# Maltese
    mt = Language(code="mt")
    mt.fullname = u'Maltese'
    mt.nplurals = '4'
    mt.pluralequation = '(n==1 ? 0 : n==0 || ( n%100>1 && n%100<11) ? 1 : (n%100>10 && n%100<20 ) ? 2 : 3)'
    mt.save()

# Nahuatl
#    nah.fullname = u'Nahuatl'
#    nah.nplurals = '2'
#    nah.pluralequation = '(n != 1)'

# Bokmål
# Norwegian Bokmal
#    nb.fullname = u'Norwegian Bokmal'
#    nb.nplurals = '2'
#    nb.pluralequation = '(n != 1)'

# Nepali
#    ne.fullname = u'Nepali'
#    ne.nplurals = u'2'
#    ne.pluralequation = u'(n != 1)'

# Nederlands
# Dutch
    nl = Language(code="nl")
    nl.fullname = u'Dutch; Flemish'
    nl.nplurals = '2'
    nl.pluralequation = '(n != 1)'
    nl.save()

# Nynorsk
# Norwegian Nynorsk
#    nn.fullname = u'Norwegian Nynorsk'
#    nn.nplurals = '2'
#    nn.pluralequation = '(n != 1)'

# Sesotho sa Leboa
# Northern Sotho
#    nso.fullname = u'Northern Sotho'
#    nso.nplurals = '2'
#    nso.pluralequation = '(n > 1)'
#    nso.specialchars = "šŠ"

# Oriya
#    or.fullname = u'Oriya'
#    or.nplurals = '2'
#    or.pluralequation = '(n != 1)'

# Punjabi
#    pa.fullname = u'Panjabi; Punjabi'
#    pa.nplurals = '2'
#    pa.pluralequation = '(n != 1)'

# Papiamento
#    pap.fullname = u'Papiamento'
#    pap.nplurals = '2'
#    pap.pluralequation = '(n != 1)'

# Polski
# Polish
    pl = Language(code="pl")
    pl.fullname = u'Polish'
    pl.nplurals = '3'
    pl.pluralequation = '(n==1 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2)'
    pl.save()

# Pashto
# FIXME the plurals don't seem right but that is what is out in the field
#    ps = Language(code="ps")
#    ps.fullname = u'Pushto; Pashto'
#    ps.nplurals = '2'
#    ps.pluralequation = '(n != 1)'
#    ps.save()

# Português
# Portuguese
    pt = Language(code="pt")
    pt.fullname = u'Portuguese'
    pt.nplurals = '2'
    pt.pluralequation = '(n != 1)'
    pt.save()

# Português do Brasil
# Brazilian Portuguese
    pt_BR = Language(code="pt_BR")
    pt_BR.fullname = u'Portuguese (Brazil)'
    pt_BR.nplurals = '2'
    pt_BR.pluralequation = '(n > 1)'
    pt_BR.save()

# Română
# Romanian
    ro = Language(code="ro")
    ro.fullname = u'Romanian'
    ro.nplurals = '3'
    ro.pluralequation = '(n==1 ? 0 : (n==0 || (n%100 > 0 && n%100 < 20)) ? 1 : 2);'
    ro.save()

# Русский
# Russian
    ru = Language(code="ru")
    ru.fullname = u'Russian'
    ru.nplurals = '3'
    ru.pluralequation = '(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2)'
    ru.save()

# Slovenčina
# Slovak
    sk = Language(code="sk")
    sk.fullname = u'Slovak'
    sk.nplurals = '3'
    sk.pluralequation = '(n==1) ? 0 : (n>=2 && n<=4) ? 1 : 2'
    sk.save()

# Slovenščina
# Slovenian
    sl = Language(code="sl")
    sl.fullname = u'Slovenian'
    sl.nplurals = '4'
    sl.pluralequation = '(n%100==1 ? 0 : n%100==2 ? 1 : n%100==3 || n%100==4 ? 2 : 3)'
    sl.save()

# Shqip
# Albanian
    sq = Language(code="sq")
    sq.fullname = u'Albanian'
    sq.nplurals = '2'
    sq.pluralequation = '(n != 1)'
    sq.save()

# Српски / Srpski
# Serbian
    sr = Language(code="sr")
    sr.fullname = u'Serbian'
    sr.nplurals = '3'
    sr.pluralequation = '(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2)'
    sr.save()

# Sesotho
# Sotho
    st = Language(code="st")
    st.fullname = u'Sotho, Southern'
    st.nplurals = '2'
    st.pluralequation = '(n != 1)'
    st.save()

# Svenska
# Swedish
    sv = Language(code="sv")
    sv.fullname = u'Swedish'
    sv.nplurals = '2'
    sv.pluralequation = '(n != 1)'
    sv.save()

# தமிழ்
# Tamil
#    ta.fullname = u'Tamil'
#    ta.nplurals = '2'
#    ta.pluralequation = '(n != 1)'

# Туркмен / تركمن
# Turkmen
#    tk.fullname = u'Turkmen'
#    tk.nplurals = '2'
#    tk.pluralequation = '(n != 1)'

# Türkçe
# Turkish
    tr = Language(code="tr")
    tr.fullname = u'Turkish'
    tr.nplurals = '1'
    tr.pluralequation = '0'
    tr.save()

# Українська
# Ukrainian
    uk = Language(code="uk")
    uk.fullname = u'Ukrainian'
    uk.nplurals = '3'
    uk.pluralequation = '(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2)'
    uk.save()

# Tshivenḓa
# Venda
#    ve.fullname = u'Venda'
#    ve.nplurals = '2'
#    ve.pluralequation = '(n != 1)'
#    ve.specialchars = "ḓṋḽṱ ḒṊḼṰ ṅṄ"

# Vietnamese
    vi = Language(code="vi")
    vi.fullname = u'Vietnamese'
    vi.nplurals = '1'
    vi.pluralequation = '0'
    vi.save()

# Wolof
    wo = Language(code="wo")
    wo.fullname = u'Wolof'
    wo.nplurals = '2'
    wo.pluralequation = '(n != 1)'
    wo.save()

# Walon
# Walloon
#    wa.fullname = u'Waloon'
#    wa.nplurals = '2'
#    wa.pluralequation = '(n > 1)'

# 简体中文
# Simplified Chinese (China mainland used below, but also used in Singapore and Malaysia)
    zh_CN = Language(code="zh_CN")
    zh_CN.fullname = u'Chinese (China)'
    zh_CN.nplurals = '1'
    zh_CN.pluralequation = '0'
    zh_CN.specialchars = u"←→↔×÷©…—‘’“”【】《》"
    zh_CN.save()

# 繁體中文
# Traditional Chinese (Hong Kong used below, but also used in Taiwan and Macau)
    zh_HK = Language(code="zh_HK")
    zh_HK.fullname = u'Chinese (Hong Kong)'
    zh_HK.nplurals = '1'
    zh_HK.pluralequation = '0'
    zh_HK.specialchars = u"←→↔×÷©…—‘’“”「」『』【】《》"
    zh_HK.save()

# 繁體中文
# Traditional Chinese (Taiwan used below, but also used in Hong Kong and Macau)
    zh_TW = Language(code="zh_TW")
    zh_TW.fullname = u'Chinese (Taiwan)'
    zh_TW.nplurals = '1'
    zh_TW.pluralequation = '0'
    zh_TW.specialchars = u"←→↔×÷©…—‘’“”「」『』【】《》"
    zh_TW.save()

# This is a "language" that gives people access to the (untranslated) template files
    templates = Language(code="templates")
    templates.fullname = u'Templates'
    templates.save()

def create_default_users():
    """Create the default user(s) for Pootle. You definitely want to change
    the admin account so that your default install is not accessible with the
    default credentials. The users 'noboby' and 'default' should be left as is."""
    admin = User(username=u"admin",
                first_name=u"Administrator",
                is_active=True,
                is_superuser=True,
                is_staff=True)
    admin.set_password("admin")
    admin.save()

    # The nobody user is used to represent an anonymous user in cases where
    # we need to associate model information with such a user. An example is
    # in the permission system: we need a way to store rights for anonymous
    # users; thus we use the nobody user.
    nobody = User(username=u"nobody",
                first_name=u"any anonymous user",
                is_active=True)
    nobody.set_unusable_password()
    nobody.save()

    # The default user represents any valid, non-anonymous user and is used to
    # associate information any such user. An example is in the permission
    # system: we need a way to store default rights for users. We use the
    # default user for this.
    #
    # In a future version of Pootle we should think about using Django's 
    # groups to do better permissions handling.
    default = User(username=u"default",
                 first_name=u"any authenticated user",
                 is_active=True)
    default.set_unusable_password()
    default.save()