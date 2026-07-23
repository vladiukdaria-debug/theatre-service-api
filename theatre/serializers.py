from django.db import transaction
from rest_framework import serializers

from theatre.models import (
    Actor,
    Genre,
    Performance,
    Play,
    Reservation,
    TheatreHall,
    Ticket,
)


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = (
            "id",
            "first_name",
            "last_name",
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            "id",
            "name",
        )


class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = (
            "id",
            "title",
            "description",
            "actors",
            "genres",
        )


class PlayListSerializer(PlaySerializer):
    actors = ActorSerializer(
        many=True,
        read_only=True,
    )
    genres = GenreSerializer(
        many=True,
        read_only=True,
    )


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = (
            "id",
            "name",
            "rows",
            "seats_in_row",
        )


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = (
            "id",
            "play",
            "theatre_hall",
            "show_time",
        )


class PerformanceListSerializer(PerformanceSerializer):
    play = serializers.CharField(
        source="play.title",
        read_only=True,
    )
    theatre_hall = serializers.CharField(
        source="theatre_hall.name",
        read_only=True,
    )


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            "id",
            "row",
            "seat",
            "performance",
        )

    def validate(self, attrs):
        performance = attrs["performance"]
        row = attrs["row"]
        seat = attrs["seat"]

        hall = performance.theatre_hall

        if row > hall.rows:
            raise serializers.ValidationError(
                {
                    "row": (
                        f"Row must be between 1 and "
                        f"{hall.rows}"
                    )
                }
            )

        if seat > hall.seats_in_row:
            raise serializers.ValidationError(
                {
                    "seat": (
                        f"Seat must be between 1 and "
                        f"{hall.seats_in_row}"
                    )
                }
            )

        if Ticket.objects.filter(
            performance=performance,
            row=row,
            seat=seat,
        ).exists():
            raise serializers.ValidationError(
                "This seat is already reserved."
            )

        return attrs


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(
        many=True,
        allow_empty=False,
    )

    class Meta:
        model = Reservation
        fields = (
            "id",
            "created_at",
            "tickets",
        )
        read_only_fields = (
            "id",
            "created_at",
        )

    @transaction.atomic
    def create(self, validated_data):
        tickets_data = validated_data.pop("tickets")

        reservation = Reservation.objects.create(
            user=self.context["request"].user
        )

        for ticket_data in tickets_data:
            Ticket.objects.create(
                reservation=reservation,
                **ticket_data,
            )

        return reservation
