from django.db import models
from flourish_facet.choices import OFTEN_DONE
from ..model_mixins import CrfModelMixin
from edc_base.model_validators.date import date_not_future
from edc_base.utils import age, get_utcnow
from edc_constants.choices import YES_NO


class InfantBehaviourQuestionnaire(CrfModelMixin):

    dob = models.DateField(
        verbose_name='Child date of birth',
        help_text="Must match labour and delivery report.",
        validators=[date_not_future])

    child_age = models.IntegerField(
        verbose_name='Child age in weeks?',
        help_text='(Weeks)',)

    dressed_squirm = models.CharField(
        verbose_name=('When being dressed or undressed during the last week,'
                      'how often did the baby squirm and/or try to roll away?'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=('Fa one omo apesa kana omo apola mo bekeng ee fitileng ,'
                   'go diragetse gakae gore ngwana a sute kana a leke go pitikologa?')
    )
    tossed_laugh = models.CharField(
        verbose_name=(
            'When tossed around playfully how often did the baby laugh?'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=('Fa omo kapisa go diragetse gakae gore ngwana a tshege?')
    )
    tired_distress = models.CharField(
        verbose_name=('When tired,how often did your baby show distress?'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=(
            'Fa a lapile ,go diragetse gakae gore a supe gosa tseege sentle?')
    )
    unfamilar_adult_cling = models.CharField(
        verbose_name=('When introduced to an unfamiliar adult'
                      'how often did the baby cling to a parent?'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=('Fa omo itsise mogolo yo asa mo itseng,go diragetse gakae gore abo '
                   'a siela/a itshwarella ka wena motsadi wa gagwe?')
    )
    enjoy_read = models.CharField(
        verbose_name=(
            'How often during the last week did the baby enjoy being read to?'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=(
            'Go diragetse gakae mo bekeng ee fetileng gore ngwana a itumelele go balelwa?')
    )
    play_toy = models.CharField(
        verbose_name=('How often during the last week did the baby'
                      ' play with one toy or object for 5-10 minutes?'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=('Go diragetse gakae mo bekeng ee fetileng gore ngwana a tshameke ka ditoy kgotsa sengwe mo lebakeng '
                   'la metsotso ee metlhano goya kogo Lesome? ')
    )
    move_towards_objects = models.CharField(
        verbose_name=('How often during the last week did your baby '
                      'move quickly towards new objects?'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=(
            'Go diragetse gakae mo bekeng ee fitileng gore ngwana a atumele ka befefo ko dilong tse disha?')
    )
    water_laugh = models.CharField(
        verbose_name=(
            'When put in bath water how often did the baby laugh or enjoy it?,'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=(
            'Fa a tsenngwa mo metsing a a tlhapang ,go diragetse gakafe  gore  ngwana   a tshege kana a itumele?')
    )

    nap_whimper = models.CharField(
        verbose_name=('When it was time for bed or a nap and your baby did not want to go,'
                      'how often did s/he whimper or sob?'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=('Fa ele nako ya go robala kana ya go tshwabanya ,mme  ngwana wa gago a sa batle go '
                   'tsamaya,go diragetse  gakae gore abo a lela lela?')
    )
    after_sleep_cry = models.CharField(
        verbose_name=(
            'After sleeping how often did the baby cry if someone doesnt come within a few minutes?'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=(
            'Fa a sena go tsoga,go diragetse gakae gore abo a lela fa mongwe a sa tle mo sebakeng sa metsotsonyana?')
    )
    feeding_get_away = models.CharField(
        verbose_name=('In the last week,while being fed in your lap how often did the baby seem'
                      ' eager to get away as soon as the feeding was over'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=('Mo bekeng ee fetileng,fa a  jesiwa ale mo diropeng tsa gago,go diragetse gakae '
                   'gore ngwana a supe fa a batla  tota go tsamaya  morago fela fa a fetsa go jesiwa?')
    )
    sing_soothe = models.CharField(
        verbose_name=(
            'When singing or talking to your baby,how often did s/he soothe immediately,'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=(
            'Fa o opela kana o bua le ngwana wa gago,go diragetse gakae gore a iketle gone foo?')
    )
    put_on_back = models.CharField(
        verbose_name=('When placed on his/her back,'
                      'how often did the baby squirm and/or turn body?'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=(
            'Fa o mmaya ka mokwata,go diragetse gakae  gore a itseneke(sutesute) kana a retolose mmele?')
    )
    peackaboo_laugh = models.CharField(
        verbose_name=(
            'During a peekaboo game ,how often did the baby laugh?'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=(
            'Ka nako ya motshameko wa go iphitha,go diragetse gakae  gore ngwana a tshege?')
    )
    lookup_telephone = models.CharField(
        verbose_name=(
            'How often does the infant look around when the cell phone rings?'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=(
            'Go diragetse gakae gore  ngwana a lebe kwa kwa fa  mogala o lela?')
    )
    angry_crib = models.CharField(
        verbose_name=(
            'How often did the baby seem angry (crying and fussing) when you left her/him where the baby sleeps?'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=(
            'Go diragetse gakae gore ngwana a lebege a tenegile (a lela kana a amegile)fa o mo tlogetse fa a robalang teng?')
    )
    startle_body_position = models.CharField(
        verbose_name=('How often during the last week did your baby startle at '
                      'sudden change in body position(e.g., when moved suddenly)'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=('Go diragetse gakae mo bekeng ee fetileng gore ngwana a nne le go tshoga'
                   ' (sekai,fa  a fetolwa ka bonako ka fa a neng a ntse ka teng?')
    )
    enjoy_words = models.CharField(
        verbose_name=('How often during the last week did your baby enjoy hearing'
                      ' the sound of words,as in stories or nursery rhymes?'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=('Go diragetse gakae mo bekeng ee fetileng gore ngwana wa gago a'
                   ' itumelele go utlwa medumo ya mafoko ,jaaka mo dipolelong tsa bana?')
    )
    look_books = models.CharField(
        verbose_name=('How often during the last week did your baby look at pictures'
                      ' in books ans/or on a phone for 5 minutes or longer at a time?'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=('Go diragetse gakae mo bekeng ee fetileng gore ngwana a lebe '
                   'ditshwantsho mo bukeng kana mo mogaleng lebaka la metsotso ee metlhano kana go feta?')
    )
    visit_exicited = models.CharField(
        verbose_name=('When visiting a new place,how often did your baby get excited'
                      ' about exploring new surrondings?'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=('Fa le etetse lefelo le lesha ,go diragetse gakae gore ngwana a itumelele'
                   ' go ka ithuta le go feta ka tikilogo e ntsha?')
    )
    toy_laugh = models.CharField(
        verbose_name=('How often during the last week did the baby smile or laugh'
                      ' when given a toy?'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=('Go diragetse gakae mo bekeng ee fetileng gore ngwana a ntshe monyenyo kana'
                   ' a tshege fa o mo fa selo se a tshamekang ka sone/toy?')
    )
    exciting_day_tearful = models.CharField(
        verbose_name=(
            'At the end of an exciting day,how often did your baby become tearful or cry/almost cry?'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=(
            'Fa letsatsi lele itumedisang le fela,go diragetse gakae gore ngwana a lele kgotsa a batle go lela?')
    )
    protest_confinement = models.CharField(
        verbose_name=('How often did the last week did the baby protest being placed'
                      ' in a confining place (in the back-go belega)?'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=('Go diragetse gakae mo bekeng ee fetile gore ngwana a itwele '
                   'fa o mmaya mo lefelong lele sa phuthologang  (go belegwa)?')
    )
    held_enjoy = models.CharField(
        verbose_name=('When being held in the last week,did your baby seem to'
                      ' enjoy him/herself?'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=(
            'Fa omo tshwere,mo bekeng ee fetileng,a ngwana one a supa a itumetse?')
    )
    look_at_soothe = models.CharField(
        verbose_name=('When showing the baby something to look at,'
                      'how often did s/he soothe immediately?'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=(
            'Fa omo supegetsa sengwe se aka se lebang,a ngwana one a iketa gone foo?')
    )
    hair_wash_vocalize = models.CharField(
        verbose_name=(
            'When the babys head was washed ,how often did the baby vocalize/make words?'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=(
            'Fa o mo tlhapisa tlhogo ,go diragetse gakae gore abo a leka go ntsha mafoko?')
    )
    airplane_sound = models.CharField(
        verbose_name=(
            'How often did your baby notice the sound of an airplane passing overhead?'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=(
            'Go diragetse gakae gore ngwana a lemoge modumo wa sefofane se feta ko godimo?')
    )
    unfamilar_adult_refuse = models.CharField(
        verbose_name=('When introduced to an unfamiliar adult'
                      'how often did the baby refuse to go to the unfamilar person?'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=(
            'Fa o mo itsise mogolo yo asa mo itseng,go diragetse gakae gore ngwana a gane go ya ko go ene?')
    )
    activity_often_cry = models.CharField(
        verbose_name=('When you were busy with another activity,and your baby was not able to get'
                      ' your attention ,how often did s/he cry?'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=('Fa one o tshwerwe ke tiro e nngwe/o santse o dira  sengwe,'
                   'ngwana asa kgone go bona nako ya gago,go  diragetse gakae gore  a lele?')
    )
    enyoy_swaying = models.CharField(
        verbose_name=('How often during the last week did the baby enjoy gentle rhythmic activities'
                      ' such as rocking or swaying?'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=('Go diragetse gakae mo bekeng ee fetileng gore ngwana a itumelele go tshameka mogo '
                   'bonolo ,jaaka go tshikinngwa mogo bonolo/go kungkuretswa ?')
    )
    stare_picture = models.CharField(
        verbose_name=('How often during the last week did the baby stare at a cell phone'
                      'picture,or bed bumper for 5 minutes or longer'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=('Go diragetse gakae mo bekeng ee fetileng gore ngwana  a tlhome'
                   ' matlho a gagwe mo mogaleng,ditshwantsho kana mo diphatsaneng tsa gagwe  lebaka la metsotso ee metlhano kgotsa go feta?')
    )
    wanted_upset = models.CharField(
        verbose_name=('When the baby wanted something,how often did s/he become upset'
                      'when s/he could not get what s/he wanted?'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=(
            'Fa ngwana a batla sengwe ,go diragetse gakae gore a tenege fa a sa kgone go fiwa se ase batlang?')
    )
    unfamilar_adult_cling_again = models.CharField(
        verbose_name=('When in the presence of unfamiliar adults '
                      'how often did the baby cling to a parent?'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=('Fa ale fa bagolong bale mmalwa ba asa ba itseng,go diragetse'
                   ' gakae gore a ingangatele ka motsadi wa gagwe?')
    )
    enyoy_rocking = models.CharField(
        verbose_name=(
            'When you rocked or hugged in the last week, did your baby seem enjoy him/herself?'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=(
            'Fa o mo tshamekisa kana omo atla,mo bekeng ee fetileng,a ngwana one a lebega a itumela?')
    )
    rubbing_soothe = models.CharField(
        verbose_name=('When patting or gently rubbing some parts of the babys body,'
                      'how often did s/he soothe immediately'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=('Fa o  phophotha kana o tshwara mo dikarolong dingwe tsa mmele wa ngwana,'
                   'go diragetse gakae gore a iketle gone foo?')
    )
    take_outside = models.CharField(
        verbose_name='Do you bring your baby anywhere outside',
        choices=YES_NO,
        max_length=5,
        help_text='A o etle O tshwele le ngwana gope kwa ntle?'
    )
    talking_sound = models.CharField(
        verbose_name=(
            'How often did your baby make talking sounds when he/she was outside?'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=(
            'Go diragetse gakae gore ngwana a dire medumo e nkareng o a bua fa le dule mo lwapeng?')
    )
    blanket_squirm = models.CharField(
        verbose_name=('When placed in a blanket seat'
                      'how often did the baby squirm and turn body?'),
        choices=OFTEN_DONE,
        max_length=15,
        help_text=('Fa o mmaya omo tshegela  ,go diragetse gakae '
                   'gore ngwana a itseneke a bo a retolola mmele?')
    )

    comment = models.TextField(
        null=True,
        blank = True)

    @property
    def get_child_age(self):
        child_age = age(self.dob, get_utcnow())
        age_in_weeks = (child_age.years * 52) + \
            (child_age.months * 4) + child_age.days // 7

        return age_in_weeks

    def save(self, *args, **kwargs):
        self.child_age = self.get_child_age
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'flourish_facet'
        verbose_name = 'Infant Behaviour Questionnaire'
        verbose_name_plural = 'Infant Behaviour Questionnaire'
