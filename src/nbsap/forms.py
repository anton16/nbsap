from django import forms
from django.conf import settings
from django.forms import widgets
from django.shortcuts import get_object_or_404
from django.conf import settings
from tinymce.widgets import TinyMCE

from pagedown.widgets import PagedownWidget
from models import NationalStrategy, NationalObjective, NationalAction, \
                   AichiTarget, AichiGoal, EuAction, EuTarget


class NationalObjectiveForm(forms.Form):
    language = forms.ChoiceField(choices=settings.LANGUAGES)
    title = forms.CharField(widget=widgets.Textarea)
    description = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 25}), required=False)

    def __init__(self, *args, **kwargs):

        self.objective = kwargs.pop('objective', None)
        self.parent_objective = kwargs.pop('parent_objective', None)
        lang = kwargs.pop('lang', None)

        super(NationalObjectiveForm, self).__init__(*args, **kwargs)

        if self.objective:
            title = getattr(self.objective, 'title_%s' % lang, None)
            description = getattr(self.objective,
                                  'description_%s' % lang, None)

            self.fields['title'].initial = title
            self.fields['description'].initial = description
            self.fields['language'].initial = lang

    def save(self):

        objective = self.objective or NationalObjective()
        lang = self.cleaned_data['language']
        title = self.cleaned_data['title']
        description = self.cleaned_data['description']

        setattr(objective, 'title_%s' % lang, title)
        setattr(objective, 'description_%s' % lang, description)

        if self.parent_objective:
            objective.parent = self.parent_objective

        objective.save()

        return objective


class NationalActionForm(forms.Form):
    language = forms.ChoiceField(choices=settings.LANGUAGES)
    description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 25}))

    def __init__(self, *args, **kwargs):

        self.action = kwargs.pop('action', None)
        self.objective = kwargs.pop('objective')
        lang = kwargs.pop('lang', None)

        super(NationalActionForm, self).__init__(*args, **kwargs)

        description = getattr(self.action, 'description_%s' % lang, None)

        self.fields['description'].initial = description
        self.fields['language'].initial = lang

    def save(self):

        action = self.action or NationalAction()
        lang = self.cleaned_data['language']
        description = self.cleaned_data['description']

        setattr(action, 'description_%s' % lang, description)
        setattr(action, 'code', self.objective.code)

        action.save()
        action.objective = [self.objective]

        action.save()

        return action


class NationalStrategyForm(forms.Form):

    def get_my_choices(string, mytype, goal=None):
        return [(element.pk,
                 "%s %s" % (string, element.code.upper())) for element in mytype.objects.all()]

    def get_element_by_pk(self, mytype, u_pk):
        return mytype.objects.filter(pk=int(u_pk)).all()[0]

    nat_objective = forms.ChoiceField(choices=get_my_choices('Objective',
                                                             NationalObjective))
    aichi_goal = forms.ChoiceField(choices=get_my_choices('Goal', AichiGoal))
    aichi_target = forms.ChoiceField(choices=get_my_choices('Target',
                                                            AichiTarget))
    other_targets = forms.MultipleChoiceField(choices=get_my_choices('Target', AichiTarget),
                                              required=False)

    if settings.EU_STRATEGY:
        eu_targets = forms.MultipleChoiceField(choices=get_my_choices('Target', EuTarget),
                                               required=False)
        eu_actions = forms.MultipleChoiceField(choices=get_my_choices('Action', EuAction),
                                               required=False)

    def __init__(self, *args, **kwargs):
        self.strategy = kwargs.pop('strategy', None)
        super(NationalStrategyForm, self).__init__(*args, **kwargs)

        if self.strategy:
            self.fields['nat_objective'].initial = self.strategy.objective.pk
            self.fields['aichi_goal'].initial = self.strategy.relevant_target.get_parent_goal().pk
            self.fields['aichi_target'].initial = self.strategy.relevant_target.pk
            self.fields['other_targets'].initial = [target.pk for target in self.strategy.other_targets.all()]
            if settings.EU_STRATEGY:
                self.fields['eu_targets'].initial = [target.pk for target in self.strategy.eu_targets.all()]
                self.fields['eu_actions'].initial = [action.id for action in self.strategy.eu_actions.all()]

    def save(self):
        strategy = self.strategy or NationalStrategy()
        nat_obj = self.get_element_by_pk(
            NationalObjective, self.cleaned_data['nat_objective'])
        aichi_targ = self.get_element_by_pk(
            AichiTarget, self.cleaned_data['aichi_target'])

        setattr(strategy, 'objective', nat_obj)
        setattr(strategy, 'relevant_target', aichi_targ)
        strategy.save()

        strategy.other_targets.clear()
        if settings.EU_STRATEGY:
            strategy.eu_targets.clear()
            strategy.eu_actions.clear()

        for ucode in self.cleaned_data['other_targets']:
            strategy.other_targets.add(get_object_or_404(AichiTarget,
                                                         code=ucode))
        if settings.EU_STRATEGY:
            for ucode in self.cleaned_data['eu_targets']:
                strategy.eu_targets.add(get_object_or_404(EuTarget, code=ucode))
            for ucode in self.cleaned_data['eu_actions']:
                strategy.eu_actions.add(get_object_or_404(EuAction, pk=ucode))

        strategy.save()
        return strategy
