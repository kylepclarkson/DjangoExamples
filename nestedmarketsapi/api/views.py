
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from .serializers import MatchListSerializer, MatchDetailSerializer
from .models import Match, Sport, Selection, Market


class MatchViewSet(viewsets.ModelViewSet):

    queryset = Match.objects.all()
    serializer_class = MatchListSerializer # for list view
    detail_serializer_class = MatchDetailSerializer # for detail view
    # filter_backends = (DjangoFilterBackend, OrderingFilter,)
    ordering_fields = '__all__'

    def get_serializer_class(self):
        # Determine which serializer to use.
        if self.action == 'retrieve':
            if hasattr(self, 'detail_serializer_class'):
                return self.detail_serializer_class
        # default is MatchListSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        # Filter again 'sport' and 'name' query parameter.
        queryset = Match.objects.all()
        sport = self.request.query_params.get('sport', None)
        name = self.request.query_params.get('name', None)
        if sport:
            sport = sport.title()
            queryset = queryset.filter(sport__name=sport)
        if name:
            queryset = queryset.filter(name=name)
        return queryset

    def create(self, request, *args, **kwargs):
        """
        Parse request and create a new match or update its odds.
        """
        # print('Request')
        import json
        print(json.dumps(request.data, indent=4))
        message = request.data.pop('message_type')
        if message == 'NewEvent':
            # Create new match.
            event = request.data.pop('event')
            sport = event.pop('sport')
            market = event.pop('market')[0]   # only single market
            selections = market.pop('selections')
            # create sport, markets, and selections
            sport = Sport.objects.create(**sport)
            market = Market.objects.create(**market, sport=sport)
            for selection in selections:
                market.selections.create(**selection)
            # Create match
            match = Match.objects.create(**event, sport=sport, market=market)
            return Response(status=status.HTTP_201_CREATED)
        elif message == 'UpdateSelection':
            market = request.data.pop('market')[0]
            match = Match.objects.get(id=request.data.pop('id'))

            new_selection = request.data.pop('new_selection')
            
            for selection in match.market.selections.all():
                selection.delete()    
            match.market.selections.create(**new_selection)

            return Response(status=status.HTTP_201_CREATED)
        elif message == 'UpdateOdds':
            # Update odds
            event = request.data.pop('event')
            market = event.pop('market')[0]
            selections = market.pop('selections')
            for selection in selections:
                s = Selection.objects.get(id=selection.get('id'))
                s.odds = selection.get('odds')
                s.save()
            match = Match.objects.get(id=event.get('id'))
            return Response(status=status.HTTP_201_CREATED)
        elif message == 'UpdateSportName':
            event = request.data.pop('event')
            sport = event.pop('sport')
            print("sport\n", sport)
            sportUpdate = Sport.objects.get(id=sport.pop('id'))
            sportUpdate.name = sport.pop('name')
            sportUpdate.save()
            return Response(status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


