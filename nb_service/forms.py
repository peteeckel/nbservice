from django import forms

from dcim.models import Device
from circuits.models import Circuit, Provider
from tenancy.models import Tenant
from ipam.models import Service
from virtualization.models import VirtualMachine
from utilities.forms import BootstrapMixin
from utilities.forms.fields import DynamicModelMultipleChoiceField, DynamicModelChoiceField, CSVModelMultipleChoiceField
from utilities.forms.widgets import DatePicker

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelImportForm,
)

from . import utils
from . import models

class ServiceForm(BootstrapMixin, forms.ModelForm):

    clients = DynamicModelMultipleChoiceField(label="Clients",
        queryset=Tenant.objects.all(),
        required=False,
    )

    backup_profile = forms.CharField(required=False)

    class Meta:
        model = models.Service
        fields = [
            "name",
            "clients",
            "comments",
            "backup_profile",
        ]

class ApplicationForm(BootstrapMixin, forms.ModelForm):

    devices = DynamicModelMultipleChoiceField(label="Devices",
        queryset=Device.objects.all(),
        required=False,
    )
    vm = DynamicModelMultipleChoiceField(label="Virtual Machines",
        queryset=VirtualMachine.objects.all(),
        required=False,
    )


    class Meta:
        model = models.Application
        fields = [
            "name",
            "protocol",
            "ports",
            "version",
            "devices",
            "vm",
        ]

class ICForm(BootstrapMixin, forms.ModelForm):

    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
    )
    virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
    )

    application = utils.DynamicModelChoiceField(
        queryset=models.Application.objects.all(),
        required=False,
    )

    class Meta:
        model = models.IC
        fields = [
            'service',
        ]


class PenTestForm(BootstrapMixin, forms.ModelForm):

    class Meta:
        model = models.PenTest
        fields = [
            'service',
            'comments',
            'status',
            'date',
            'ticket',
            "report_link",
        ]

        widgets = {
            'date': DatePicker(),
        }

class RelationForm(BootstrapMixin, forms.ModelForm):

    source = utils.DynamicModelChoiceField(
        queryset=models.IC.objects.all(),
        required=True,
        label='Source',
        query_params={
            'service_id': '$service',
        },
        display_field='name',
    )

    destination = utils.DynamicModelChoiceField(
        queryset=models.IC.objects.all(),
        required=True,
        label='Destination',
        query_params={
            'service_id': '$service',
        },
        display_field='name',
    )

    link_text = forms.CharField(required=False)

    class Meta:
        model = models.Relation
        fields = [
            'service',
            'source',
            'source_shape',
            'destination',
            'destination_shape',
            "connector_shape",
            "link_text",
        ]

class ServiceFilterForm(BootstrapMixin, forms.ModelForm):

    q = forms.CharField(
        required=False,
        label='Search'
    )
    clients = DynamicModelMultipleChoiceField(
        label="Clients",
        queryset=Tenant.objects.all(),
        required=False,
    )

    class Meta:
        model = models.Service
        fields = [
            'q',
            'clients',
        ]

class ServiceBulkEditForm(NetBoxModelBulkEditForm):
    model = models.Service

    clients = DynamicModelMultipleChoiceField(
        label="Clients",
        queryset=Tenant.objects.all(),
        required=False,
    )
    comments = forms.Textarea(
        attrs={'class': 'font-monospace'}
    )
    backup_profile = forms.CharField(
        required=False,
    )

    class Meta:
        nullable_fields = ("clients", "comments", "backup_profile")

class ServiceImportForm(NetBoxModelImportForm):
    clients = CSVModelMultipleChoiceField(
        label="Clients",
        queryset=Tenant.objects.all(),
        required=False,
        to_field_name="name",
        error_messages={
            "invalid_choice": "Client name not found",
        }
    )

    class Meta:
        model = models.Service
        fields = ["name", "clients", "comments", "backup_profile"]


class ApplicationFilterForm(BootstrapMixin, forms.ModelForm):

    q = forms.CharField(
        required=False,
        label='Search'
    )
    devices = DynamicModelMultipleChoiceField(label="Devices",
        queryset=Device.objects.all(),
        required=False,
    )

    virtual_machines = DynamicModelMultipleChoiceField(label="Virtual Machines",
        queryset=VirtualMachine.objects.all(),
        required=False,
    )

    class Meta:
        model = models.Service
        fields = [
            'q',
            'devices',
            'virtual_machines',
        ]
