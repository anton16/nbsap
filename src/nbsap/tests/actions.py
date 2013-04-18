# -*- coding: utf-8 -*client.-
from django.test.client import Client
from django.utils import unittest
from django.test import TestCase
from django.contrib.auth.models import User

from nbsap import models

class NationalActionTestCase(TestCase):
    fixtures = ['initial_data.json',]

    def setUp(self):
        # create a user to test with
        self.user = User.objects.create_user('admin', 'admin@admin.com', 'q')
        self.client = Client()
        # blind call to set user info on session
        call = self.client.post('/accounts/login/', {'username': 'admin',
                                                     'password': 'q'})

    def test_list_national_action(self):
        """ Listing National objective 1.1's actions """
        response = self.client.get('/administration/objectives/16')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Actions related to objective 1.1', response.content)

    def test_view_national_action(self):
        """ Test the view of national action """
        response = self.client.get('/administration/objectives/16/actions/1/')
        self.assertEqual(response.status_code, 200)
        content = response.content
        self.assertIn("Biological Evaluation Maps (BWK)", content)

    def test_edit_national_action(self):
        """ Test editing national action for objective's 1.1 """
        mydata = {
            'language': 'en',
            'description': 'My new description'
        }

        response = self.client.get('/administration/objectives/16/actions/1/edit')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/administration/objectives/16/actions/1/edit', mydata)
        edited_object = models.NationalAction.objects.all().filter(id=1)[0]
        self.assertEqual(edited_object.description, mydata['description'])

    def test_edit_national_action_with_encodings(self):
        """ Test editing national action for Objective 1.1's """
        mydata = {
            'language': 'en',
            'description': u'ĂFKĐȘKŁFKOKR–KF:ŁĂȘĐKF–KFÂŁ:FJK–FFŁKJȘĂŁF'
        }

        response = self.client.get('/administration/objectives/16/actions/1/edit')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/administration/objectives/16/actions/1/edit', mydata)
        edited_object = models.NationalAction.objects.all().filter(id=1)[0]
        self.assertEqual(edited_object.description, mydata['description'])

    def test_add_national_action(self):
        """ Test national action adding """
        mydata = {
            'objective': {
                            'language': 'en',
                            'title': 'My new objective title',
                            'description': 'My new objective description'
            },
            'action': {
                        'language': 'en',
                        'description': 'My new action description'
                }

        }
        # add an objective first
        response = self.client.get('/administration/objectives/add/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/administration/objectives/add/', mydata['objective'])
        added_object = models.NationalObjective.objects.all().filter(code='16')[0]
        self.assertEqual(added_object.title, mydata['objective']['title'])
        self.assertEqual(added_object.description, mydata['objective']['description'])

        # secondly, add a specific action
        response = self.client.get('/administration/objectives/101/actions/add')
        self.assertEqual(response.status_code, 200)

        self.client.post('/administration/objectives/101/actions/add', mydata['action'])
        added_action = models.NationalAction.objects.filter(id=78)[0]
        self.assertEqual(added_action.description, mydata['action']['description'])


        # clean the mess by deleting the action
        action_id = str(added_action.id)
        response = self.client.get('/administration/objectives/101/actions/%s/delete' % action_id)

        # clean the mess by deleting the objective
        response = self.client.get('/administration/objectives/%s/delete' % (str(added_object.id)))

    def test_add_national_action_with_encodings(self):
        """ Test national action adding with encodings """
        mydata = {
            'objective': {
                            'language': 'en',
                            'title': 'My new objective title',
                            'description': 'My new objective description'
            },
            'action': {
                        'language': 'en',
                        'description': u'ĂFKĐȘKŁFKOKR–KF:ŁĂȘĐKF–KFÂŁ:FJK–FFŁKJȘĂŁF'
            }

        }
        # add an objective first
        response = self.client.get('/administration/objectives/add/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/administration/objectives/add/', mydata['objective'])
        added_object = models.NationalObjective.objects.all().filter(code='16')[0]
        self.assertEqual(added_object.title, mydata['objective']['title'])
        self.assertEqual(added_object.description, mydata['objective']['description'])

        # secondly, add a specific action
        objective_id = str(added_object.id)
        response = self.client.get('/administration/objectives/%s/actions/add' % objective_id)
        self.assertEqual(response.status_code, 200)

        self.client.post('/administration/objectives/%s/actions/add' % objective_id, mydata['action'])
        added_action = models.NationalAction.objects.filter(code=16)[0]
        self.assertEqual(added_action.description, mydata['action']['description'])

        # clean the mess by deleting the action
        action_id = str(added_action.id)
        response = self.client.get('/administration/objectives/101/actions/%s/delete' % action_id)

        # clean the mess by deleting the objective
        response = self.client.get('/administration/objectives/%s/delete' % (str(added_object.id)))

    def test_delete_national_action(self):
        """ Test national action deleting - Objective 1.2's action deleted """

        _object = models.NationalAction.objects.all().filter(id='2')[0]
        self.assertIn('fauna of the Brussels Capital Region.', _object.description)

        response = self.client.get('/administration/objectives/17/actions/2/delete')

        try:
            _object = models.NationalAction.objects.all().filter(id='2')[0]
        except:
            pass
        else:
            # something went wrong when deleting
            self.assertEqual(1,2)

    def tearDown(self):
         self.user.delete()