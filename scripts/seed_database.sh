#!/bin/bash

set -e
cd "$(dirname "$0")/.."

seed_teams() {
    local count=$1
    python src/manage.py seed_teams --count "$count"
}

seed_users() {
    local team_ids=$1
    local users_min=$2
    local users_max=$3
    local user_ids=""
    local team_array

    IFS=',' read -ra team_array <<< "$team_ids"

    for team_id in "${team_array[@]}"; do
        local user_count=$((RANDOM % (users_max - users_min + 1) + users_min))

        local team_user_ids
        team_user_ids=$(python src/manage.py seed_users --count $user_count --team-id "$team_id")

        if [ -n "$user_ids" ]; then
            user_ids="$user_ids,$team_user_ids"
        else
            user_ids="$team_user_ids"
        fi
    done
    echo "$user_ids"
}

seed_categories() {
    local count=$1
    python src/manage.py seed_categories --count "$count"
}

seed_assignment_targets() {
    local count=$1
    python src/manage.py seed_assignment_targets --count "$count"
}

seed_assignments() {
    local category_ids=$1
    local target_ids=$2
    local assignments_min=$3
    local assignments_max=$4
    local category_array
    local target_array

    IFS=',' read -ra category_array <<< "$category_ids"
    IFS=',' read -ra target_array <<< "$target_ids"

    for category_id in "${category_array[@]}"; do
        for target_id in "${target_array[@]}"; do
            local assignment_count=$((RANDOM % (assignments_max - assignments_min + 1) + assignments_min))
            python src/manage.py seed_assignments --count $assignment_count --category-id "$category_id" --target-id "$target_id"
        done
    done
}

seed_playbook_assignments() {
    local user_ids=$1
    local category_ids=$2
    local playbooks_min=$3
    local playbooks_max=$4
    local user_array
    local category_array

    IFS=',' read -ra user_array <<< "$user_ids"
    IFS=',' read -ra category_array <<< "$category_ids"

    for user_id in "${user_array[@]}"; do
        for category_id in "${category_array[@]}"; do
            local playbook_count=$((RANDOM % (playbooks_max - playbooks_min + 1) + playbooks_min))

            if [ $playbook_count -gt 0 ]; then
                python src/manage.py seed_playbook_assignments --count $playbook_count --category-id "$category_id" --user-id "$user_id"
            fi
        done
    done
}

echo "🌱 Starting database seeding..."

echo "👥 Seeding teams..."
TEAM_IDS=$(seed_teams 10)
echo "  ✓ Created teams: $TEAM_IDS"

echo "🧑 Seeding users for each team..."
USER_IDS=$(seed_users "$TEAM_IDS" 20 40)
echo "  ✓ Created users: $USER_IDS"

echo "🏷️ Seeding categories..."
CATEGORY_IDS=$(seed_categories 10)
echo "  ✓ Created categories: $CATEGORY_IDS"

echo "🎯 Seeding assignment targets..."
TARGET_IDS=$(seed_assignment_targets 10)
echo "  ✓ Created assignment targets: $TARGET_IDS"

echo "📝 Seeding assignments..."
seed_assignments "$CATEGORY_IDS" "$TARGET_IDS" 2 5

echo "📖 Seeding playbook assignments..."
seed_playbook_assignments "$USER_IDS" "$CATEGORY_IDS" 0 2

echo ""
echo "✅ Database seeding completed successfully!"