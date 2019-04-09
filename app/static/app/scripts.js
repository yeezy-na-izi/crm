document.addEventListener('DOMContentLoaded', function() {
    var sidenavElems = document.querySelectorAll('.sidenav');
    var sideNavInst = M.Sidenav.init(sidenavElems, {});

    var collapsibleElem = document.querySelectorAll('.collapsible');
    var collapsibleInstance = M.Collapsible.init(collapsibleElem, {});

    var tabsElem = document.querySelectorAll('.tabs');
    var instance = M.Tabs.init(tabsElem, {});

    var selectElems = document.querySelectorAll('select');
    var selectInst = M.FormSelect.init(selectElems, {});

    var dropDownElems = document.querySelectorAll('.dropdown-trigger.perms-role-select');
    var dropDownInst = M.Dropdown.init(dropDownElems, {
        constrainWidth: false,
        closeOnClick: false
    });

    var dateElems = document.querySelectorAll('.datepicker');
    var dateInstances = M.Datepicker.init(dateElems, {format: 'dd.mm.yyyy'});

    var timeElems = document.querySelectorAll('.timepicker');
    var timeInstances = M.Timepicker.init(timeElems, {twelveHour: false});
});
