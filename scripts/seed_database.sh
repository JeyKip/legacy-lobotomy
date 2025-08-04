#!/bin/bash

set -e
cd "$(dirname "$0")/.."

# Fixed parent entity counts
TEAMS_COUNT=10
CATEGORIES_COUNT=10
TARGETS_COUNT=10

# Random ranges for child entities
USERS_MIN=20
USERS_MAX=40
ASSIGNMENTS_MIN=5
ASSIGNMENTS_MAX=10
PLAYBOOKS_MIN=0
PLAYBOOKS_MAX=2

echo "🌱 Starting database seeding..."

echo "👥 Seeding teams..."
TEAM_IDS=$(python src/manage.py seed_teams --count $TEAMS_COUNT)
echo "  ✓ Created teams: $TEAM_IDS"

echo "🧑 Seeding users for each team..."
IFS=',' read -ra TEAM_ARRAY <<< "$TEAM_IDS"
USER_IDS=""
TOTAL_USERS=0

for team_id in "${TEAM_ARRAY[@]}"; do
    # Generate random number of users for this team
    user_count=$((RANDOM % (USERS_MAX - USERS_MIN + 1) + USERS_MIN))
    TOTAL_USERS=$((TOTAL_USERS + user_count))

    # Create users for this team
    team_user_ids=$(python src/manage.py seed_users --count $user_count --team-id "$team_id")

    # Append to total user IDs
    if [ -n "$USER_IDS" ]; then
        USER_IDS="$USER_IDS,$team_user_ids"
    else
        USER_IDS="$team_user_ids"
    fi

    echo "  ✓ Created $user_count users for the team $team_id"
done
echo "  ✓ Created $TOTAL_USERS users"

echo "🏷️ Seeding categories..."
CATEGORY_IDS=$(python src/manage.py seed_categories --count $CATEGORIES_COUNT)
echo "  ✓ Created categories: $CATEGORY_IDS"

echo "🎯 Seeding assignment targets..."
TARGET_IDS=$(python src/manage.py seed_assignment_targets --count $TARGETS_COUNT)
echo "  ✓ Created assignment targets: $TARGET_IDS"

echo "📝 Seeding assignments..."
IFS=',' read -ra CATEGORY_ARRAY <<< "$CATEGORY_IDS"
IFS=',' read -ra TARGET_ARRAY <<< "$TARGET_IDS"
TOTAL_ASSIGNMENTS=0

for category_id in "${CATEGORY_ARRAY[@]}"; do
    for target_id in "${TARGET_ARRAY[@]}"; do
        # Generate random number of assignments for this combination
        assignment_count=$((RANDOM % (ASSIGNMENTS_MAX - ASSIGNMENTS_MIN + 1) + ASSIGNMENTS_MIN))
        TOTAL_ASSIGNMENTS=$((TOTAL_ASSIGNMENTS + assignment_count))

        # Create assignments for this category + target combination
        python src/manage.py seed_assignments --count $assignment_count --category-id "$category_id" --target-id "$target_id"

        echo "  ✓ Created $assignment_count assignments for the category $category_id and target $target_id"
    done
done
echo "  ✓ Created $TOTAL_ASSIGNMENTS assignments"

echo "📖 Seeding playbook assignments..."
IFS=',' read -ra USER_ARRAY <<< "$USER_IDS"
TOTAL_PLAYBOOKS=0

for user_id in "${USER_ARRAY[@]}"; do
    for category_id in "${CATEGORY_ARRAY[@]}"; do
        # Generate random number of playbook assignments for this user and category
        playbook_count=$((RANDOM % (PLAYBOOKS_MAX - PLAYBOOKS_MIN + 1) + PLAYBOOKS_MIN))

        # Only create playbooks if count is greater than 0
        if [ $playbook_count -gt 0 ]; then
            TOTAL_PLAYBOOKS=$((TOTAL_PLAYBOOKS + playbook_count))

            # Create playbook assignments for this user and category
            python src/manage.py seed_playbook_assignments --count $playbook_count --category-id "$category_id" --user-id "$user_id"

            echo "  ✓ Created $playbook_count playbooks for the user $user_id and category $category_id"
        fi
    done
done
echo "  ✓ Created $TOTAL_PLAYBOOKS playbook assignments"

echo ""
echo "✅ Database seeding completed successfully!"
echo ""
echo "Summary:"
echo "  • ${#TEAM_ARRAY[@]} teams with $TOTAL_USERS total users"
echo "  • $TOTAL_ASSIGNMENTS total assignments distributed across ${#CATEGORY_ARRAY[@]} categories and ${#TARGET_ARRAY[@]} assignment targets"
echo "  • $TOTAL_USERS users with $TOTAL_PLAYBOOKS total playbook assignments"