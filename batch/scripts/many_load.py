import csv  # https://docs.python.org/3/library/csv.html

# https://django-extensions.readthedocs.io/en/latest/runscript.html

# python3 manage.py runscript many_load
from unesco.models import Category, State, Iso, Region, Site


def run():
    fhand = open('unesco/whc-sites-2018-clean.csv')
    reader = csv.reader(fhand)
    next(reader)  # Advance past the header

    Category.objects.all().delete()
    State.objects.all().delete()
    Iso.objects.all().delete()
    Region.objects.all().delete()
    Site.objects.all().delete()

    # Format
    # name, category, state, region, iso

    for row in reader:
        print(row)

        c, created = Category.objects.get_or_create(name=row[7])
        st, created = State.objects.get_or_create(name=row[8])
        r, created = Region.objects.get_or_create(name=row[9])
        i, created = Iso.objects.get_or_create(name=row[10])

        try:
            y = int(row[3])
        except:
            y = None

        a = row[6]
        if a == '':
            a = None

        site = Site (name=row[0], description=row[1], justification=row[2], year=y, longitude=row[4], latitude=row[5], area_hectares=a, category=c, region=r, iso=i, state=st)
        site.save()
# from unesco.models import Person, Course, Membership


# def run():
#     fhand = open('many/load.csv')
#     reader = csv.reader(fhand)
#     next(reader)  # Advance past the header

#     Person.objects.all().delete()
#     Course.objects.all().delete()
#     Membership.objects.all().delete()

#     # Format
#     # email,role,course
#     # jane@tsugi.org,I,Python
#     # ed@tsugi.org,L,Python

#     for row in reader:
#         print(row)

#         p, created = Person.objects.get_or_create(email=row[0])
#         c, created = Course.objects.get_or_create(title=row[2])

#         r = Membership.LEARNER
#         if row[1] == 'I':
#             r = Membership.INSTRUCTOR
#         m = Membership(role=r, person=p, course=c)
#         m.save()