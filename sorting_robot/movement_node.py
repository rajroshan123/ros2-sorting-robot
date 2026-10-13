
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String


class MovementNode(Node):

    def __init__(self):
        super().__init__('movement_node')

        self.publisher = self.create_publisher(
            Twist, '/cmd_vel', 10
        )

        self.subscription = self.create_subscription(
            String,
            '/sorting_decision',
            self.decision_callback,
            10
        )

        self.movement_timer = self.create_timer(
            0.1, self.control_robot
        )

        self.motion = 'STOP'
        self.start_time = None
        self.duration = 0.0
        self.last_decision = None

        self.get_logger().info('Movement node started.')

    def decision_callback(self, msg):
        decision = msg.data

        if decision not in ('BIN_1', 'BIN_2', 'BIN_3'):
            return

        if self.motion != 'STOP':
            return

        if decision == self.last_decision:
            self.get_logger().info(
                f'Ignoring repeated decision: {decision}'
            )
            return

        self.last_decision = decision
        self.start_time = self.get_clock().now()

        if decision == 'BIN_1':
            self.motion = 'LEFT'
            self.duration = 1.5
            self.get_logger().info('BIN_1: turning left.')

        elif decision == 'BIN_2':
            self.motion = 'STRAIGHT'
            self.duration = 2.0
            self.get_logger().info('BIN_2: moving straight.')

        elif decision == 'BIN_3':
            self.motion = 'RIGHT'
            self.duration = 1.5
            self.get_logger().info('BIN_3: turning right.')

    def control_robot(self):
        command = Twist()

        if self.motion != 'STOP':
            elapsed = (
                self.get_clock().now() - self.start_time
            ).nanoseconds / 1e9

            if elapsed < self.duration:
                if self.motion == 'LEFT':
                    command.angular.z = 0.5

                elif self.motion == 'STRAIGHT':
                    command.linear.x = 0.1

                elif self.motion == 'RIGHT':
                    command.angular.z = -0.5

            else:
                self.motion = 'STOP'
                self.get_logger().info('Motion complete. Robot stopped.')

        self.publisher.publish(command)

    def destroy_node(self):
        self.publisher.publish(Twist())
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = MovementNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
